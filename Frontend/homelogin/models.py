from django.db import models

# Create your models here.

class Settings(models.Model):
    follow_message = models.CharField(max_length=200)
    timeout_time = models.IntegerField()
    freq_viewer_time = models.IntegerField()

class Search(models.Model):
    search_text = models.CharField(max_length=200)

class Title(models.Model):
    broadcast_title = models.CharField(max_length=200)
    game = models.CharField(max_length=200)
