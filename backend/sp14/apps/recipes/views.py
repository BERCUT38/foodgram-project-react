from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.pagination import CustomPageNumberPaginator

from .filters import RecipeFilter
from .models import Favorite, Recipes, Ringredients, ShoppingList
from .permissions import IsAuthorOrAdmin
from .serializers import (AddRecipeSerializer, FavouriteSerializer,
                          FullRecipesSerializer, ShoppingListSerializer)


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
        user_shopping_list = ShoppingList.objects.filter(user=request.user)
        to_buy = get_ingredients_list(user_shopping_list)
        return download_file_response(to_buy, 'to_buy.txt')

    def destroy(self, request, pk):
        recipe = Recipes.objects.get(id=pk)
        recipe.delete()
        return Response('Рецепт успешно удален', status=status.HTTP_200_OK)


def get_ingredients_list(recipes_list):
    ingredients_dict = {}
    for recipe in recipes_list:
        ingredients = Ringredients.objects.filter(recipe=recipe.recipe)
        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurment_unit = ingredient.ingredient.measurment_unit
            if name not in ingredients_dict:
                ingredients_dict[name] = {
                    'measurment_unit': measurment_unit,
                    'amount': amount
                }
            else:
                ingredients_dict[name]['amount'] += amount
    to_buy = []
    for item in ingredients_dict:
        to_buy.append(f'{item}-{ingredients_dict[item]["amount"]}'
                      f'{ingredients_dict[item]["measurment_unit"]} \n')
    return to_buy


def download_file_response(list_to_download, filename):
    response = HttpResponse(list_to_download, 'Content-Type: text/plain')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
