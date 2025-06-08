from django.db import models

# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=255)

    def __str(self):
        return self.room_name
    
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    message = models.TextField()
    file = models.FileField(upload_to='uploads/', null=True, blank=True)  # New field for file uploads

    def __str__(self):
        return f"{self.sender} in {self.room}"