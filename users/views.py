from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from users.models import Follow, User
from users.serializers import UserSerializer, UserListSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserProfilesView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    @action(
        methods=["POST"],
        detail=True,
        url_path="follow"
    )
    def follow_user(self, request, pk=None):
        user_to_follow = self.get_object()

        if user_to_follow == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not request.user.following.filter(id=pk).exists():
            Follow.objects.create(
                follower=request.user, following=user_to_follow
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["POST"],
        detail=True,
        url_path="unfollow"
    )
    def unfollow_user(self, request, pk=None):
        get_object_or_404(get_user_model(), id=pk)
        request.user.following.filter(id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
