from django.db import models
from classes.models import Class

class Assignment(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    
    def __str__(self):
        return f"{self.title} - {self.class_obj.title}"