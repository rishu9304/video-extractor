from django.db import models

# Create your models here.
class TrackVideoProgress(models.Model):
    name = models.CharField(max_length=255, null=False)
    file = models.FileField(upload_to="videos/")
    status = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
