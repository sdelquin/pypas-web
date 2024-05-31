from django.contrib import admin

from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise', 'passed', 'created_at', 'updated_at']
