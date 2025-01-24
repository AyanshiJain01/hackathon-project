from django.contrib import admin

# Register your models here.
# jobs/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, JobPost, JobApplication

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'location')
    list_filter = ('user_type', 'location')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'location', 'about', 'profile_picture')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(JobPost)
admin.site.register(JobApplication)
