from django.contrib import admin

from .models import Context, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'token', 'context']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Context)
class ContextAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
