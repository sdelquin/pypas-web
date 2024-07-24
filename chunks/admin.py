from django.contrib import admin

from .models import Chunk


@admin.register(Chunk)
class ChunkAdmin(admin.ModelAdmin):
    list_display = ['frame', 'exercise', 'puttable']
    autocomplete_fields = ['exercise']
