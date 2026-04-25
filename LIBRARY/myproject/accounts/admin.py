from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.contrib.admin.models import LogEntry
from .models import User

# Register Custom User with its special fields
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Overriding fieldsets to remove password and other technical fields from edit page
    fieldsets = (
        (None, {'fields': ('username', 'role', 'status')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'department')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'role', 'status', 'password'), # Password only needed during creation
        }),
    )

    list_display = ('id', 'username', 'role', 'date_joined', 'status', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('role', 'status', 'is_staff', 'is_superuser', 'is_active')


# Registering system tables so Admin can directly manage them all in one place
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'codename')
    search_fields = ('name', 'codename')
    list_filter = ('content_type',)

@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ('app_label', 'model')
    search_fields = ('model', 'app_label')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'expire_date', 'get_decoded')
    search_fields = ('session_key',)

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag')
    search_fields = ('object_repr', 'change_message')
    list_filter = ('action_flag', 'content_type')
