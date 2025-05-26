from django.contrib import admin
from .models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'class_obj', 'enrolled_at')
    search_fields = ('user__email', 'class_obj__title')