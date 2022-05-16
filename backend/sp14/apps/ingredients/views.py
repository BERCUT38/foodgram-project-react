from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, mixins

from .models import Ingredient
from .serializers import IngredientSerializer
from .filters import IngredientsFilter


class RetriveAndListViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    pass


class IngredientViewSet(RetriveAndListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter
    pagination_class = None
