from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Dog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dogname = models.CharField(max_length=100)
    age = models.IntegerField()
    sex = models.CharField(max_length=100)
    introduction = models.CharField(max_length=255)
    image = models.ImageField(upload_to="dogs/")
    like_num = models.IntegerField(default=0)

class Crew(models.Model):
    users = models.ManyToManyField(User, verbose_name='ユーザー')
    name = models.CharField(max_length=20)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
