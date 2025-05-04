from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Chunk


@admin.action(description='Add selected chunks to frame')
def add_chunks_to_frame(modeladmin, request, queryset):
    chunk_ids = queryset.values_list('id', flat=True)
    query_string = f'?chunk_ids={",".join(str(id) for id in chunk_ids)}'
    return HttpResponseRedirect(reverse('chunks-admin:add-chunks-to-frame') + query_string)


@admin.register(Chunk)
class ChunkAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['exercise', 'frame', 'exercise_topic', 'puttable', 'hits', 'order']
    autocomplete_fields = ['exercise']
    search_fields = ['exercise__slug']
    list_filter = ['frame', 'exercise__topic', 'puttable']
    actions = [add_chunks_to_frame]

    @admin.display(description='Topic')
    def exercise_topic(self, obj) -> str:
        return obj.exercise.topic
