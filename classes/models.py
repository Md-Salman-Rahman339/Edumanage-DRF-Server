from django.db import models
from users.models import User

class Class(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    title = models.CharField(max_length=255)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classes_taught')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    short_description = models.TextField()
    total_enrolment = models.PositiveIntegerField(default=0)
    image = models.URLField(max_length=500, blank=True)  # For storing image URLs
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='approved')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class MyClass(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    title = models.CharField(max_length=255)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_classes')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    short_description = models.TextField()
    total_enrolment = models.PositiveIntegerField(default=0)
    image = models.URLField(max_length=500, blank=True)  # For storing image URLs
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='approved')
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return self.title