

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "phone", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "email", "phone", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "phone", "password1", "password2", "is_staff", "is_active")}
        ),
    )
    search_fields = ("username", "email")
    ordering = ("username",)
