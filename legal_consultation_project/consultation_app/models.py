from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Lawyer(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=100)  # Password should be encrypted
    is_verified = models.BooleanField(default=False)
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
    professional_certificate = models.FileField(upload_to='lawyer_certificates/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='lawyer_profiles/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.specialization}"


#model to handle news and artical

class LegalArticle(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='legal_news_images/', null=True, blank=True)
    published_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title



class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



class Consultation(models.Model):
    # Defining choices for the consultation status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),  
    ]

    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='consultations')
    lawyer = models.ForeignKey('Lawyer', on_delete=models.CASCADE, related_name='consultations')
    message = models.TextField(blank=True, null=True, help_text="Optional message from client to lawyer")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    is_client_notified = models.BooleanField(default=False)  # New field
    is_lawyer_notified = models.BooleanField(default=False)  # New field
    scheduled_time = models.DateTimeField(null=True, blank=True, help_text="Scheduled date and time for the consultation")
    message_from_lawyer = models.TextField(blank=True, null=True, help_text="Message or instructions from the lawyer")
    room = models.ForeignKey('ChatApp.room', on_delete=models.SET_NULL, null=True, blank=True, related_name='consultations')

    def __str__(self):
        return f"Consultation Request from {self.client} to {self.lawyer} - {self.status}"
    
    def get_video_room_name(self):
        return f"video_consult_{self.pk}"

    class Meta:
        ordering = ['-requested_at']




class Notification(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notification for {self.client} - {self.message[:30]}"







class Feedback(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    comment = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.client}"