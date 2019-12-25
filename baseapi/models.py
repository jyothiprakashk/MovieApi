from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title=models.CharField(verbose_name='movie_name',max_length=30)
    overview=models.TextField(blank=True, null=True)
    release=models.DateField()
    poster=models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    vote_average=models.CharField(max_length=30,default=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.title

    