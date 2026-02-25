from django.contrib import admin
from .models import Task, UserProfile

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'completed', 'user', 'created_at', 'updated_at']
    list_filter = ['completed', 'created_at', 'user']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email']