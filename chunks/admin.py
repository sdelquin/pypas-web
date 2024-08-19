from django.contrib import admin

from .models import Chunk


@admin.register(Chunk)
class ChunkAdmin(admin.ModelAdmin):
    list_display = ['frame', 'exercise', 'exercise_topic', 'puttable', 'int_order']
    autocomplete_fields = ['exercise']
    search_fields = ['exercise__slug']
    list_filter = ['frame__context', 'frame__bucket', 'exercise__topic', 'puttable']

    @admin.display(description='Order')
    def int_order(self, obj) -> int:
        iorder = int(obj.order)
        return iorder if iorder == obj.order else obj.order

    @admin.display(description='Topic')
    def exercise_topic(self, obj) -> str:
        return obj.exercise.topic
