from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Follow
from .serializers import FollowSerializer, ShowFollowSerializer
from apps.pagination import CustomPageNumberPaginator

User = get_user_model()


def respons_subscribe(items):
    key, val = items
    if key in ('user', 'following'):
        return False
    return True


class FollowApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, id):
        data = {'user': request.user.id, 'following': id}
        serializer = FollowSerializer(
            data=data, context={'request': request}
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        sd = serializer.data
        ser_resp = dict(filter(respons_subscribe, sd.items()))
        return Response(
            ser_resp,
            status=status.HTTP_201_CREATED
            )

    def delete(self, request, id):
        user = request.user
        following = get_object_or_404(User, id=id)
        subscription = get_object_or_404(Follow, user=user,
                                         following=following
                                         )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListFollowViewSet(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ShowFollowSerializer
    pagination_class = CustomPageNumberPaginator

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)
