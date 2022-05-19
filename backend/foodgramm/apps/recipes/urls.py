from rest_framework.routers import DefaultRouter

from .views import RecipesViewSet

recipes_router = DefaultRouter()
recipes_router.register('', RecipesViewSet, basename='recipes')
