from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from activities.models import Post, PostLikes
from activities.serializers import (
    PostSerializer,
    PostListSerializer,
    PostDetailSerializer
)


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = (
        Post.objects.select_related("user")
        .annotate(all_likes=Count("likes"))
    )
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        content = self.request.query_params.get("content")

        if content:
            queryset = queryset.filter(content__icontains=content)

        if self.action == "list":
            queryset = queryset.filter(
                Q(user__id=self.request.user.id)
                | Q(user__id__in=self.request.user.following.values("following_id"))
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer

        if self.action == "retrieve":
            return PostDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        methods=["POST"],
        detail=True
    )
    def like(self, request, pk=None):
        new_like, created = PostLikes.objects.get_or_create(
            user=request.user, post_id=pk
        )
        if not created:
            new_like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        url_path="liked"
    )
    def get_all_liked_posts(self, request, pk=None):
        posts = Post.objects.filter(likes__user=self.request.user)
        serializer = PostListSerializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
