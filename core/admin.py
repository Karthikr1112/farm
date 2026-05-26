from django.contrib import admin
from .models import Inquiry

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'category', 'product', 'status', 'created_at')
    list_filter = ('status', 'category', 'product')
    search_fields = ('name', 'phone', 'message')
    ordering = ('-created_at',)
