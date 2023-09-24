from rest_framework import serializers

from social_media.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author",
            "liked_by",
            "created_at",
            "updated_at",
        ]


class PostCreateSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
        ]


class PostListSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author",
            "liked_by",
            "created_at",
            "updated_at",
        ]
