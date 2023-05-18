Video Subtile Extractor
The Subtitle Extractor is a Django app that allows users to extract subtitles from various types of video files. It provides an easy-to-use interface for uploading video files and extracting the corresponding subtitle files.

## Features

- Extract subtitles from popular video formats (e.g., MP4, AVI, MKV).
- Support for multiple subtitle formats (e.g., SRT, VTT, ASS).
- User-friendly web interface for uploading videos and retrieving subtitles.
- Automatic detection and extraction of embedded or external subtitle tracks.
- Download and save extracted subtitle files for future use.

## Requirements

- Python 3.8 or above
- Django 3.2 or above
- Redis

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/django-app.git
```

2. Activate Virtual Environment.
3. Install dependencies.

```bash
pip install -r requirements.txt
```
4. Create a .env file and populate value from .env.example file.
5. Run the database migration.
```bash
python manage.py makemigrations
python manage.py migrate
```
6. Start the server
```bash
python manage.py runserver
```
7. Make sure redis-server is running.
8. Start celery

```bash
celery -A video_subtitle_extractor worker -B -l info -Q parse_video
```

Urls
1. `/video-upload/`: Upload video to parse it.
2. `/video-list/`: Show parse video with search field.
3. `search-text/`: API to get subtitles of video from the search string.