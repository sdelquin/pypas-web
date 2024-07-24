from django.contrib import admin

from .models import Bucket, Frame


@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    list_display = ['context', 'bucket', 'start', 'end', 'num_exercises']
    filter_horizontal = ('exercises',)


@admin.register(Bucket)
class BucketAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
