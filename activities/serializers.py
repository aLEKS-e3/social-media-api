from rest_framework import serializers

from activities.models import Post, Comment
from users.models import Follow
from users.serializers import UserDetailSerializer


class PostSerializer(serializers.ModelSerializer):
    schedule_time = serializers.DateTimeField(write_only=True, allow_null=True)

    class Meta:
        model = Post
        fields = ("id", "image", "content", "created_at", "schedule_time",)


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("id", "image", "content", "created_at",)


class PostListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    all_likes = serializers.IntegerField(read_only=True)
    all_comments = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "image",
            "content",
            "user",
            "created_at",
            "all_likes",
            "all_comments"
        )


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("id", "body",)


class CommentDetailSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "body", "user", "created_at",)


class PostDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    comments = CommentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "image",
            "content",
            "user",
            "created_at",
            "likes",
            "comments",
        )


class FollowingListSerializer(serializers.ModelSerializer):
    following_username = serializers.CharField(
        source="following.username", read_only=True
    )
    following_profile_picture = serializers.CharField(
        source="following.profile_image", read_only=True
    )

    class Meta:
        model = Follow
        fields = ("id", "following_username", "following_profile_picture",)


class FollowerListSerializer(serializers.ModelSerializer):
    follower_username = serializers.CharField(
        source="follower.username", read_only=True
    )
    follower_profile_picture = serializers.CharField(
        source="follower.profile_image", read_only=True
    )

    class Meta:
        model = Follow
        fields = ("id", "follower_username", "follower_profile_picture",)
