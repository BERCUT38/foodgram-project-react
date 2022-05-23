from rest_framework.routers import DefaultRouter

from .views import TagsViewSet

tags_router = DefaultRouter()
tags_router.register('', TagsViewSet, basename='tags')
