from rest_framework import serializers

from social_media.models import Post, Comment


class CommentListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(many=False, read_only=True, slug_field="email")
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "content", "author", "like_count", "created_at", "updated_at"]


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "content"]


class PostSerializer(serializers.ModelSerializer):
    liked_by = serializers.SlugRelatedField(many=True, read_only=True, slug_field="email")
    author = serializers.SlugRelatedField(many=False, read_only=True, slug_field="email")

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
            "image"
        ]


class PostCreateSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "image"
        ]


class PostListSerializer(PostSerializer):
    comments = serializers.SlugRelatedField(many=True, read_only=True, slug_field="content")
    author = serializers.SlugRelatedField(many=False, read_only=True, slug_field="email")
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author",
            "like_count",
            "created_at",
            "updated_at",
            "comments",
            "image"
        ]
