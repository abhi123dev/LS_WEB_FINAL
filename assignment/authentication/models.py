from django.db import models
from django.utils import timezone

# Create your models here.
from django.contrib.auth.models import User

class Tweet(models.Model):
    user = models.ForeignKey(User , on_delete = models.SET_NULL , null = True , blank = True)
    name = models.CharField(max_length=100)
    content = models.TextField()
    tweet_image = models.ImageField(upload_to="tweets/")
    created_at = models.DateTimeField(default=timezone.now )
    def __str__(self):
        return self.user