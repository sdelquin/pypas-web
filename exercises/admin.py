from django.contrib import admin

from .models import Exercise, Topic


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['slug', 'available', 'folder', 'topic']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['primary', 'secondary']
