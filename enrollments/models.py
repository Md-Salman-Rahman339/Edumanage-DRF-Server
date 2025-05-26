from django.db import models
from users.models import User
from classes.models import Class

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'class_obj')
    
    def __str__(self):
        return f"{self.user.email} enrolled in {self.class_obj.title}"