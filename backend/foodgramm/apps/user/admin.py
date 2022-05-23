from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']
    search_fields = ('username', 'id',) 
    list_filter = ('username',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'following']
    search_fields = ('user','id',) 
    list_filter = ('user',)
