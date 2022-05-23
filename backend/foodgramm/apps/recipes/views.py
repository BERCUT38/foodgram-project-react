import os

from apps.ingredients.models import Ingredient
from apps.pagination import CustomPageNumberPaginator

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import Favorite, Recipes, Ringredients, ShoppingList
from .permissions import IsAuthorOrAdmin
from .serializers import (AddRecipeSerializer, FavouriteSerializer,
                          FullRecipesSerializer, ShoppingListSerializer)

User = get_user_model()


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all().order_by('-id')
    serializer_class = FullRecipesSerializer
    permission_classes = [IsAuthorOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPaginator

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FullRecipesSerializer
        return AddRecipeSerializer

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=[IsAuthorOrAdmin]
        )
    def favorite(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = FavouriteSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipes, id=pk)
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=[IsAuthorOrAdmin]
        )
    def shopping_cart(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = ShoppingListSerializer(data=data,
                                            context={'request': request}
                                            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipes, id=pk)
        shopping_list = get_object_or_404(ShoppingList,
                                          user=user,
                                          recipe=recipe
                                          )
        shopping_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user.username
        user_shopping_list = request.user.shlist.all()
        return get_ingredients_list(user_shopping_list, user)

    def destroy(self, request, pk):
        recipe = Recipes.objects.get(id=pk)
        recipe.delete()
        return Response('Рецепт успешно удален', status=status.HTTP_200_OK)


def get_ingredients_list(recipes_list, user):
    recipes = [item.recipe.id for item in recipes_list]
    ingredients_list = Ringredients.objects.filter(
        recipe__in=recipes
    ).values(
        'ingredient'
    ).annotate(
        amount=Sum('amount')
    )

    filename = f'{user}_ingredients_list.txt'

    if not os.path.isdir('recipes_data/ingredients_list'):
        os.mkdir('recipes_data/ingredients_list')

    with open(f'recipes_data/ingredients_list/{filename}', 'w') as textfile:
        textfile.write('Список покупок:\n\n')
        for item in ingredients_list:
            ingredient = Ingredient.objects.get(pk=item['ingredient'])
            amount = item['amount']
            textfile.write(
                f'{ingredient.name}, {amount} '
                f'{ingredient.measurement_unit}\n'
            )
    with open(f'recipes_data/ingredients_list/{filename}', 'r') as textfile:
        response = HttpResponse(textfile.read(), content_type="text/txt")
        response['Content-Disposition'] = (
            'attachment; filename=' + filename
        )
    return response
