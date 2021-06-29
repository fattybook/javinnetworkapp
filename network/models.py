from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

## a post should have a username, description, time, number of likes
class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True)
    liked_post = models.ManyToManyField(User, related_name= "liked_pots", blank=True)
    likes = models.IntegerField(default=0)

class Follow(models.Model):
    person_of_interest = models.ForeignKey(User, on_delete=models.PROTECT, related_name="target", blank=True, null=True)
    followers = models.ManyToManyField(User, related_name="followerss", blank=True)
    following = models.ManyToManyField(User, related_name="followings", blank=True)