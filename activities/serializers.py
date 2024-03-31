from rest_framework import serializers

from activities.models import Post
from users.serializers import UserDetailSerializer


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("id", "image", "content", "created_at",)


class PostListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    all_likes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "image", "content", "user", "created_at", "all_likes",)


class PostDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "image", "content", "user", "created_at", "likes",)
