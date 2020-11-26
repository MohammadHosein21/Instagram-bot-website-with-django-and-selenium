from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    usernameIG = models.CharField(max_length=50)
    passwordIG = models.CharField(max_length=50)
    followers = models.TextField()

    def __str__(self):
        return str(self.user)


class Data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True, related_name='data')
    follower = ArrayField(models.IntegerField(), size=30, null=True)
    date = ArrayField(models.DateField(), size=30, null=True)


    def __str__(self):
        return str(self.user)
