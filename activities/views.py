from django.db.models import Q
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from activities.models import Post
from activities.serializers import PostSerializer, PostViewSerializer


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Post.objects.select_related("user")
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        content = self.request.query_params.get("content")
        queryset = self.queryset

        if content:
            queryset = queryset.filter(content__icontains=content)

        if self.action == "list":
            queryset = queryset.filter(
                Q(user__id=self.request.user.id)
                | Q(user__id__in=self.request.user.following.values("following_id"))
            )

        return queryset

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PostViewSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
