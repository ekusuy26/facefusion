from django.db import models
from django.contrib.auth.models import User
from accounts.models import Crew

# Create your models here.
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
    uploaded_at = models.DateTimeField(auto_now_add=True)
