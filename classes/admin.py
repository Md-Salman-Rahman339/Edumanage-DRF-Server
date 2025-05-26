from django.contrib import admin
from .models import Class, MyClass

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'price', 'total_enrolment', 'status')
    list_filter = ('status', 'teacher')
    search_fields = ('title', 'teacher__email')

@admin.register(MyClass)
class MyClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'status', 'created_at')
    list_filter = ('status', 'teacher')
    search_fields = ('title', 'teacher__email')