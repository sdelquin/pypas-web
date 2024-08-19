from django.contrib import admin

from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'exercise',
        'context',
        'frame',
        'passed',
        'created_at',
        'updated_at',
    ]
    list_filter = ['user__context']
    search_fields = ['chunk__exercise__slug', 'user__slug']

    @admin.display(description='User')
    def username(self, obj) -> str:
        return obj.user.name

    @admin.display(description='Exercise')
    def exercise(self, obj) -> str:
        return obj.chunk.exercise

    @admin.display(description='Context')
    def context(self, obj) -> str:
        return obj.chunk.frame.context

    @admin.display(description='Frame')
    def frame(self, obj) -> str:
        return obj.chunk.frame.bucket
