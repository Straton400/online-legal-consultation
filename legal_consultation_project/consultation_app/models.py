from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser

class Lawyer(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=100)  # Password should be encrypted

    class Meta:
        swappable = 'AUTH_USER_MODEL' # Recommended for custom user models

    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

  
    def __str__(self):
        return self.username
    
def upload_to_profile(instance, filename):
    return f'lawyers/profile_pics/{instance.lawyer.id}/{filename}'
    
class LawyerProfile(models.Model):
    lawyer = models.OneToOneField('consultation_app.Lawyer', on_delete=models.CASCADE, related_name='profile')

    full_name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(help_text="Years of experience")
    education = models.TextField()
    bio = models.TextField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to=upload_to_profile, blank=True, null=True)
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.specialization}"



class LegalNews(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    content = models.TextField()  # Full article content
    publish_date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='legal_news_images/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish_date']  # Sort by most recent first


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
