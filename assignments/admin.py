from django.contrib import admin

from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['user_alias', 'exercise', 'passed', 'created_at', 'updated_at']

    @admin.display(description='User')
    def user_alias(self, obj):
        return obj.user.alias
