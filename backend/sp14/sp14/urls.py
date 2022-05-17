from django.contrib import admin
from django.urls import include, path

from . import apps_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(apps_urls)),
]
