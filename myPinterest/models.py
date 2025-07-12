from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Pin(models.Model):
    title = models.CharField(max_length=255)
    image_url = models.URLField()
    category = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pins')
    created_at = models.DateTimeField(auto_now_add=True)

    
