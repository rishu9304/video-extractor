from celery import shared_task
import moviepy.editor as mp
import whisper
from app.models import TrackVideoProgress
from video_subtitle_extractor.settings import dynamo_db_table, aws_s3_client
import traceback
from datetime import timedelta
import os

@shared_task(bind=True, max_retries=1)
def parse_video(self, video_id, video_filename, video_file_path):
    try:
        # Convert video to audio
        print("Video processing started...")
        audio_file_path, audio_file_name = convert_video_to_audio(video_file_path, video_filename)
        print("Video processing completed...")
        # Parse text from the audio file
        print("Audo processing started...")
        srt_file_path,srt_file_name = transcribe_audio_file(audio_file_path,audio_file_name)
        print("Audo processing completed...")
        # Store extracted text into dynamo DB
        print("Text processing started...")
        store_text_into_dyamodb(video_id,srt_file_path,srt_file_name)
        print("Text processing Completed...")
        # Upload video to s3()
        print("Upload video to s3 started...")
        upload_video_to_s3(video_file_path, video_filename)
        print("Upload video to s3 completed...")
        # Update video status
        print("DB video status updated started...")
        update_video_status(video_id, "completed")
        print("DB video status updated completed...")
    except:
        update_video_status(video_id, "failed")
        traceback.print_exc()


def convert_video_to_audio(video_file_path, video_filename):
    audio_file_path = video_file_path.replace("videos", "audios")
    audio_file_name = video_filename.split(".")[0] + ".wav"

    # Initialize moviepy editor 
    clip = mp.VideoFileClip(video_file_path + "/" + video_filename)
    audio = clip.audio

    try:
        # Use the recognizer instance to recognize speech in the audio
        with audio.write_audiofile(audio_file_path + "/" + audio_file_name) as source:
            audio_data = r.record(source)
    except:
        pass

    return audio_file_path, audio_file_name


def transcribe_audio_file(audio_file_path, audio_file_name):

    srt_file_path = audio_file_path.replace("audios", "srt_files")
    srt_file_name = audio_file_name.split(".")[0] + ".srt"

    model = whisper.load_model("base") # Change this to your desired model
    print("Whisper model loaded.")
    transcribe = model.transcribe(audio=audio_file_path+"/"+audio_file_name)
    segments = transcribe['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{startTime},{endTime},{text[1:] if text[0] == ' ' else text}\n"

        with open(srt_file_path + "/" +srt_file_name, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

    return srt_file_path, srt_file_name

def store_text_into_dyamodb(video_id, srt_file_path, srt_file_name):
    # Read parse item
    with open(srt_file_path+"/"+srt_file_name) as f:
        srt_text =  f.readlines()
    # Iterating through each item and storing in dyanamo DB
    for items in srt_text:
        item = items.split(",")
        data = {
            "VideoID": video_id,
            "StartTime": item[0],
            "EndTime": item[1],
            "Text": item[2].replace("\n", "")
        }
        dynamo_db_table.put_item(TableName='Subtitles', Item=data)

def upload_video_to_s3(video_file_path, video_file_name):
    file_path = video_file_path + "/" + video_file_name
    aws_s3_client.upload_file(file_path, os.getenv("S3_BUCKET_NAME"), video_file_name)

def update_video_status(video_id, status):
    track_video = TrackVideoProgress.objects.get(id=video_id)
    track_video.status = status
    track_video.save()
