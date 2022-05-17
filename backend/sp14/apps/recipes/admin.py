from django.contrib import admin

from .models import Favorite, Recipes, Ringredients, Rtags, ShoppingList


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author']


@admin.register(Rtags)
class RtagsAdmin(admin.ModelAdmin):
    list_display = ['id', 'recipe', 'tag']


@admin.register(Ringredients)
class RingredientsAdmin(admin.ModelAdmin):
    list_display = ['id', 'recipe', 'ingredient']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipe']


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipe']

