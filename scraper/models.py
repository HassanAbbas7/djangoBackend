from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager









class Website(models.Model):
    name = models.CharField(max_length=500)
    URL = models.CharField(max_length=500)
    Logo = models.CharField(max_length=1000,null=True,blank=True)

class Data(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE , null=True, blank=True)
    Target_website= models.CharField(max_length=500,null=True,blank=True)
    URL = models.CharField(max_length=500,null=True,blank=True)
    Title = models.CharField(max_length=1000, unique=True)
    Description = models.TextField(null=True,blank=True)
    Keywords = models.TextField( null=True,blank=True)
    Text = models.TextField(    null=True,blank=True)
    Links = models.TextField(  null=True,blank=True)
    Images = models.TextField(  null=True,blank=True)
    Videos = models.TextField(  null=True,blank=True)
    Claps = models.IntegerField(default=0)
    TimeStamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.Title

    def change_claps(self, x):
        self.Claps += x
        self.save()



class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=14)
    last_name = models.CharField(max_length=14)
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True) #auto_now = True if you want to add a field like "updated_on"
    favourite_posts = models.ManyToManyField(Data, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class Claps(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_likes')
    data = models.ForeignKey(Data, on_delete=models.CASCADE, related_name='post_likes')


class Fav(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_favs')
    data = models.ForeignKey(Data, on_delete=models.CASCADE, related_name='post_favs')
