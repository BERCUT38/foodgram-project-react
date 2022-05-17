from rest_framework import mixins, permissions, viewsets

from .models import Tags
from .serializers import TagsSerializer


class RetriveAndListViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    pass


class TagsViewSet(RetriveAndListViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
