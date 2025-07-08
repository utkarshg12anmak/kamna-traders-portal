#accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Add the 'job_title' field to the existing UserAdmin fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ("Job Info", {"fields": ("job_title",)}),
    )

    # Show 'job_title' in the user list display
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'job_title',
        'is_active',
        'is_staff',
    )