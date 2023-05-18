from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_subtitle_extractor.settings')
app = Celery('video_subtitle_extractor')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.task_routes = {
    'user.task.parse_video' : {'queue': "parse_video" },
}
app.autodiscover_tasks()