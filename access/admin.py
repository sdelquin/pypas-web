from django.contrib import admin
from django.contrib.auth.models import Group as AuthGroup
from django.contrib.auth.models import User as AuthUser

from .models import Context, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'context', 'slug', 'token']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['slug', 'token']
    list_filter = ['context']


@admin.register(Context)
class ContextAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


# Hide from admin panel
# https://stackoverflow.com/a/5508920
admin.site.unregister(AuthUser)
admin.site.unregister(AuthGroup)
