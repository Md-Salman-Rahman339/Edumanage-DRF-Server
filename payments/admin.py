from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'class_obj', 'amount', 'status', 'created_at')
    list_filter = ('status', 'class_obj')
    search_fields = ('user__email', 'transaction_id')