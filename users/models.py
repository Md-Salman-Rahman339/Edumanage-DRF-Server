from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    email = models.EmailField(unique=True)
    photo = models.URLField(blank=True, null=True)

    
  
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  
    
    def __str__(self):
        return self.email
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}".strip()

class TeacherRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    experience = models.CharField(max_length=100, blank=True, null=True)  # Added
    title = models.CharField(max_length=100, blank=True, null=True)      # Added
    category = models.CharField(max_length=100, blank=True, null=True)   # Added
    
    def __str__(self):
        return f"{self.user.email} - {self.status}"