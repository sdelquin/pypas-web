from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Chunk


@admin.action(description='Add selected chunks to frame')
def add_chunks_to_frame(modeladmin, request, queryset):
    chunk_ids = queryset.values_list('id', flat=True)
    query_string = f'?chunk_ids={','.join(str(id) for id in chunk_ids)}'
    return HttpResponseRedirect(reverse('chunks-admin:add-chunks-to-frame') + query_string)


@admin.register(Chunk)
class ChunkAdmin(admin.ModelAdmin):
    list_display = ['frame', 'exercise', 'exercise_topic', 'int_order', 'puttable', 'hits']
    autocomplete_fields = ['exercise']
    search_fields = ['exercise__slug']
    list_filter = ['frame', 'exercise__topic', 'puttable']
    actions = [add_chunks_to_frame]

    @admin.display(description='Order')
    def int_order(self, obj) -> int:
        iorder = int(obj.order)
        return iorder if iorder == obj.order else obj.order

    @admin.display(description='Topic')
    def exercise_topic(self, obj) -> str:
        return obj.exercise.topic
