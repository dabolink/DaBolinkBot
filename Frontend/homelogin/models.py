from django.db import models

# Create your models here.

class Settings(models.Model):
    follow_message = models.CharField(max_length=200)
    timeout_time = models.IntegerField(max_length=100)
    freq_viewer_time = models.IntegerField(max_length=100)