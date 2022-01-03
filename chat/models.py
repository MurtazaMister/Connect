from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class GlobalRoom(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class GlobalMessage(models.Model):
    value = models.CharField(max_length=1000000)
    user = models.ForeignKey(User,on_delete=models.CASCADE) # Could've used a related name
    user_name = models.CharField(max_length=100,blank=True)
    room = models.ForeignKey(GlobalRoom,on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.now, blank=True,null=True)

# https://stackoverflow.com/questions/13390315/have-multiple-users-as-one-model-field-in-many-to-one-format-django-models
# https://docs.djangoproject.com/en/dev/topics/db/examples/many_to_many/

class PrivateRoom(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class PrivateMessage(models.Model):
    value = models.CharField(max_length=1000000)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="puser")
    user_name = models.CharField(max_length=100,blank=True)
    room = models.ForeignKey(PrivateRoom,on_delete=models.CASCADE, related_name="proom")
    time = models.DateTimeField(default=datetime.now, blank=True,null=True)