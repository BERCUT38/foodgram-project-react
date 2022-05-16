from django_filters import rest_framework as filters

from .models import Recipes


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug',
                                           label='Tags')
    is_favorited = filters.BooleanFilter(method='get_favorite',
                                         label='Favorited')
    in_shopping_cart = filters.BooleanFilter(method='get_shopping',
                                             label='in shopping list'
                                             )

    class Meta:
        model = Recipes
        fields = ('is_favorited', 'author', 'tags', 'in_shopping_cart')

    def get_favorite(self, queryset, name, value):
        if value:
            return Recipes.objects.filter(in_favorite__user=self.request.user)
        return Recipes.objects.all()

    def get_shopping(self, queryset, name, value):
        if value:
            return Recipes.objects.filter(shoppinglist__user=self.request.user)
        return Recipes.objects.all()
