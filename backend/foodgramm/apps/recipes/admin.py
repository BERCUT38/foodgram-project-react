from django.contrib import admin

from .models import Favorite, Recipes, ShoppingList


class RingredientsInLine(admin.TabularInline):
    model = Recipes.ingredients.through
    extra = 1


class RtagsInLine(admin.TabularInline):
    model = Recipes.tags.through
    extra = 1


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author']
    search_fields = ('name', 'id',)
    list_filter = ('name',)
    inlines = (RingredientsInLine, RtagsInLine)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipe']
    search_fields = ('user', 'id',)
    list_filter = ('user',)


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipe']
    search_fields = ('user', 'id',)
    list_filter = ('user',)
