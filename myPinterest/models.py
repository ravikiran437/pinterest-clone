from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Pin(models.Model):
    title = models.CharField(max_length=255)
    image_url = models.URLField()
    category = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='pins')
    created_at = models.DateTimeField(auto_now_add=True)


class SavedPin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'pin')


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'pin')


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()


class Following(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_set')
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
