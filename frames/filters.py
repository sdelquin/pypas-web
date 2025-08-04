from django.contrib import admin

from .models import Frame


class FrameStatusFilter(admin.SimpleListFilter):
    title = 'Frame Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('active', 'Active'),
            ('inactive', 'Inactive'),
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return Frame.get_frames_by_status(self.value() == 'active')
