from django.db.models import Sum
from apps.pagination import CustomPageNumberPaginator
from django.http.response import HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import Favorite, Recipes, ShoppingList
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
        user_sl = (
           request.user.shlist.recipe.all()
        )
        to_buy = self.get_ingredients_list(user_sl)
        return download_file_response(to_buy, 'to_buy.txt')

    def destroy(self, request, pk):
        recipe = Recipes.objects.get(id=pk)
        recipe.delete()
        return Response('Рецепт успешно удален', status=status.HTTP_200_OK)

    def get_ingredients_list(self, ingredient_list):
        shopping_list = (
         ingredient_list
         .order_by(self.NAME)
         .values(self.NAME, self.MEASUREMENT_UNIT)
         .annotate(total=Sum('ingredients__amount'))
        )
        ingredients_dict = ''
        for ingredient in shopping_list:
            ingredients_dict += (
                f'{ingredient[self.NAME]}'
                f' ({ingredient[self.MEASUREMENT_UNIT]})'
                f' — {ingredient["total"]}\r\n'
            )
        return ingredients_dict


def download_file_response(list_to_download, filename):
    response = HttpResponse(list_to_download, 'Content-Type: text/plain')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
