from django.contrib.auth import get_user_model
from rest_framework import serializers
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField
from accounts.models import User
from .models import Image, Comment, Like


class SmallImageSerializer(serializers.ModelSerializer):
    """
    user for the notifications
    """
    class Meta:
        model = Image
        fields = (
            'file',
        )


class CountImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = (
            'id',
            'file',
            'comment_count',
            'like_count',
        )


class FeedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'profile_image',
        )


class CommentSerializer(serializers.ModelSerializer):

    creator = FeedUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'message',
            'creator'
        )


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    creator = FeedUserSerializer()
    tags = TagListSerializerField()

    class Meta:
        model = Image
        fields = (
            'id',
            'file',
            'location',
            'caption',
            'comments',
            'like_count',
            'creator',
            'tags',
            'created_at',
        )


class InputImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = (
            'file',
            'location',
            'caption',
        )
