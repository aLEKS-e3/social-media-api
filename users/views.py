from rest_framework import generics, status, viewsets, filters

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from activities.permissions import IsOwnerOrReadOnly
from activities.serializers import (
    FollowingListSerializer,
    FollowerListSerializer
)
from users.models import Follow, User
from users.serializers import UserSerializer, UserListSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserProfilesView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ["username"]

    @action(
        methods=["POST"],
        detail=True,
        url_path="follow",
        permission_classes=(IsAuthenticated,)
    )
    def follow_user(self, request, pk=None):
        user_to_follow = self.get_object()

        if user_to_follow == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        Follow.objects.get_or_create(
            follower=request.user, following=user_to_follow
        )

        return Response(status=status.HTTP_201_CREATED)

    @action(
        methods=["DELETE"],
        detail=True,
        url_path="unfollow",
        permission_classes=(IsAuthenticated,)
    )
    def unfollow_user(self, request, pk=None):
        user_to_unfollow = self.self.get_object()
        Follow.objects.get(
            follower=request.user, following=user_to_unfollow
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["GET"],
        detail=True,
        url_path="followers"
    )
    def get_followers(self, request, pk=None):
        user = self.get_object()
        serializer = FollowerListSerializer(
            user.followers.all(), many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=True,
        url_path="following"
    )
    def get_following(self, request, pk=None):
        user = self.get_object()
        following = user.following.all()

        serializer = FollowingListSerializer(following, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
