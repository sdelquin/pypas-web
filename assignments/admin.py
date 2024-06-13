from django.contrib import admin

from .models import Assignment, Bucket, Frame


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['user_alias', 'exercise', 'passed', 'frame', 'created_at', 'updated_at']

    @admin.display(description='User')
    def user_alias(self, obj):
        return obj.user.alias


@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    list_display = ['context', 'bucket', 'start', 'end', 'num_exercises']


@admin.register(Bucket)
class BucketAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
