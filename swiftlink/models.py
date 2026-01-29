from django.db import models

# Create your models here.
# model for original url

class Url(models.Model):
    original_url = models.URLField()
    short_key = models.CharField(max_length=6, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    