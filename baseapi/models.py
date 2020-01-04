from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=50)
    email       = models.EmailField(verbose_name='email address', unique=True, max_length=244)
    first_name  = models.CharField(max_length=30, null=True, blank=True)
    def get_username(self):
        return self.email
    
    
class Movie(models.Model):
    title=models.CharField(verbose_name='movie_name',max_length=30)
    #overview=models.TextField(blank=True, null=True)
    release=models.DateField()
    poster=models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    vote_average=models.CharField(max_length=30,default=True)
    movie_id=models.IntegerField(default=True)
    admin=models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

    