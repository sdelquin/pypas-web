from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Exercise, Topic


@admin.action(description='Add selected exercises to frame')
def add_exercises_to_frame(modeladmin, request, queryset):
    exercise_ids = queryset.values_list('id', flat=True)
    query_string = f'?exercise_ids={",".join(str(id) for id in exercise_ids)}'
    return HttpResponseRedirect(reverse('exercises-admin:add-exercises-to-frame') + query_string)


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['slug', 'topic']
    search_fields = ['slug']
    list_filter = ['topic__primary', 'topic__secondary']
    actions = [add_exercises_to_frame]


@admin.register(Topic)
class TopicAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['primary', 'secondary', 'order']
