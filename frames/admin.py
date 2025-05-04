from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from django.contrib import admin

from chunks.models import Chunk

from .models import Bucket, Frame


class ChunkInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Chunk
    extra = 0
    fields = ['exercise', 'puttable', 'order']
    autocomplete_fields = ['exercise']


@admin.register(Frame)
class FrameAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ['bucket', 'context', 'start', 'end', 'num_exercises', 'active']
    list_filter = ['context', 'bucket']
    inlines = [ChunkInline]

    @admin.display(boolean=True)
    def active(self, obj) -> bool:
        return obj.is_active


@admin.register(Bucket)
class BucketAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
