from django.contrib import admin

from .models import Bucket, Frame


@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    list_display = ['context', 'bucket', 'start', 'end', 'num_exercises', 'active']
    list_filter = ['context', 'bucket']

    @admin.display(boolean=True)
    def active(self, obj) -> bool:
        return obj.is_active


@admin.register(Bucket)
class BucketAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
