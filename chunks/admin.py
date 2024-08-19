from django.contrib import admin

from .models import Chunk


@admin.register(Chunk)
class ChunkAdmin(admin.ModelAdmin):
    list_display = ['frame', 'exercise', 'puttable']
    autocomplete_fields = ['exercise']
    search_fields = ['exercise__slug']
    list_filter = ['frame__context', 'frame__bucket', 'puttable']
