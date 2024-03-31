from rest_framework import serializers

from activities.models import Post
from users.serializers import UserDetailSerializer


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("id", "image", "content",)


class PostViewSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "image", "content", "user",)
