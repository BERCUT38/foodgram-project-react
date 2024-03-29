from django.contrib import admin

from .models import Tags


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ('name',)
    list_filter = ('name',)
