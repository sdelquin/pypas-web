from django.contrib import admin

from .models import Chunk


@admin.register(Chunk)
class ChunkAdmin(admin.ModelAdmin):
    list_display = ['frame', 'exercise', 'puttable', 'int_order']
    autocomplete_fields = ['exercise']
    search_fields = ['exercise__slug']
    list_filter = ['frame__context', 'frame__bucket', 'puttable']

    @admin.display(description='Order')
    def int_order(self, obj) -> int:
        iorder = int(obj.order)
        return iorder if iorder == obj.order else obj.order
