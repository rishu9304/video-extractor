from django.urls import path
from app.views import video_upload,video_list
from app.api import SearchVideoText

# from django_email_verification import urls as mail_urls
urlpatterns = [
    path('video-upload/', video_upload, name='video-upload'),
    path('video-list/', video_list, name='video-list'),
    path('search-text/', SearchVideoText.as_view(), name='search-text'),
]