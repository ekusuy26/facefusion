from django.db import models

# Create your models here.
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='documents/', default='defo')
    photo_two = models.ImageField(upload_to='documents/', default='defo')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    out_put = models.ImageField(upload_to='mosaics/', default='defo')
    out_put_two = models.ImageField(upload_to='mosaics/', default='defo')
