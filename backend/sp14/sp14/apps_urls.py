from django.urls import include, path

from apps.tags.urls import tags_router
from apps.ingredients.urls import ingredients_router
from apps.user.urls import urlpatterns
from apps.recipes.urls import recipes_router

urlpatterns = [
    path('ingredients/', include(ingredients_router.urls)),
    path('tags/', include(tags_router.urls)),
    path('', include(urlpatterns)),
    path('recipes/', include(recipes_router.urls))
]
