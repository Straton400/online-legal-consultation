from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser

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
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)  # e.g., 'active', 'completed', 'pending'
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consultation with {self.client.name} on {self.start_time}"