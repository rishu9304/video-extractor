from django.shortcuts import render
from app.models import TrackVideoProgress
from app.task import parse_video
from django.urls import reverse
from django.http import JsonResponse
import os

# Create your views here.
def video_upload(request):
    if request.method == "POST":
        file = request.FILES.get("video")
        track_video_progress = TrackVideoProgress(name=file.name, file=file, status="in_progress")
        track_video_progress.save()
        video_id = str(track_video_progress.id)
        filename = file.name
        file_path = "." + "/".join(track_video_progress.file.url.split("/")[:-1])
        parse_video.apply_async([video_id, filename, file_path], retry=True, queue='parse_video',
            retry_policy=dict(
                max_retries=3,
                interval_start=1,
                interval_step=1,
                interval_max=6
        ))
        response_data = {'redirect_url': reverse('video-list')}
        return JsonResponse(response_data)
        
    return render(request, "videoUpload.html", {})
        

def video_list(request):
    host_url = os.getenv("HOST_URL")
    video_list =  TrackVideoProgress.objects.all()
    return render(request, "videoList.html", {"items":video_list, "host_url": host_url})
