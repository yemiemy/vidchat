from django.conf import settings
from django.db import models
from datetime import timedelta
from django.utils.timezone import now
# Create your models here.

class Room(models.Model):
    room_name = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.room_name
    
    def deletes_in_seconds(self):
        time = self.created_at + timedelta(seconds=settings.EXPIRATION_TIME_IN_SECONDS)
        query = Room.objects.get(pk=self.pk)

        # add this code
        if time < now():
            query.delete()

class RoomMember(models.Model):
    username = models.CharField(max_length=200)
    uid = models.CharField(max_length=200)
    room_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.username