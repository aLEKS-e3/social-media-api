from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from activities.models import Post, PostLikes
from activities.permissions import IsPostOwnerOrReadOnly
from activities.serializers import (
    PostSerializer,
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
)
from activities.tasks import create_scheduled_post


class PostViewSet(viewsets.ModelViewSet):
    queryset = (
        Post.objects.select_related("user")
        .annotate(
            all_likes=Count("likes"),
            all_comments=Count("comments")
        )
    )
    serializer_class = PostSerializer
    permission_classes = (IsPostOwnerOrReadOnly,)

    def get_queryset(self):
        queryset = self.queryset
        content = self.request.query_params.get("content")

        if content:
            queryset = queryset.filter(content__icontains=content)

        if self.action == "list":
            queryset = queryset.filter(
                Q(user__id=self.request.user.id)
                | Q(user__id__in=self.request.user.following.values(
                    "following_id"
                ))
            )

        if self.action == "retrieve":
            queryset = queryset.prefetch_related("comments__user")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer

        if self.action == "retrieve":
            return PostDetailSerializer

        if self.action == "comment":
            return CommentSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        user = get_user_model().objects.get(pk=user_id)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        schedule_time = request.data.get("schedule_time")

        if schedule_time:
            create_scheduled_post.apply_async(
                args=[
                    request.data.get("content"),
                    request.FILES.get("image"),
                    user_id
                ],
                eta=schedule_time
            )
            headers = self.get_success_headers(serializer.data)
            return Response(
                "Post is scheduled",
                status=status.HTTP_200_OK,
                headers=headers
            )

        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["POST"], detail=True)
    def like(self, request, pk=None):
        new_like, created = PostLikes.objects.get_or_create(
            user=request.user, post_id=pk
        )
        if not created:
            new_like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, url_path="liked")
    def get_all_liked_posts(self, request, pk=None):
        posts = Post.objects.filter(likes__user=self.request.user)
        serializer = PostListSerializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=True)
    def comment(self, request, pk=None):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        serializer.save(
            post_id=pk,
            user=self.request.user,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
