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
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100,blank=True)
    room = models.ForeignKey(GlobalRoom,on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.now, blank=True,null=True)