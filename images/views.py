from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import UserSerializer
from images.models import Image, Like, Comment
from images.serializers import ImageSerializer, InputImageSerializer, CommentSerializer, CountImageSerializer


class Images(APIView):

    def get(self, request, format=None):

        user = request.user

        following_users = user.following.all()

        image_list = []

        for following_user in following_users:

            user_images = following_user.images.all()[:2]

            for image in user_images:

                image_list.append(image)

        my_images = user.images.all()[:2]

        for image in my_images:

            image_list.append(image)

        sorted_list = sorted(image_list, key=lambda image: image.created_at, reverse=True)

        serializer = ImageSerializer(sorted_list, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):

        user = request.user

        serializer = InputImageSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(creator=user)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetail(APIView):

    def find_own_image(self, image_id, user):
        try:
            image = Image.objects.get(id=image_id, creator=user)
            return image
        except Image.DoesNotExist:
            return None

    def get(self, request, image_id, format=None):

        user = request.user

        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ImageSerializer(image)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, image_id, format=None):

        user = request.user

        image = self.find_own_image(image_id, user)

        if image is None:

            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = InputImageSerializer(image, data=request.data, partial=True)

        if serializer.is_valid():

            serializer.save(creator=user)

            return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)

        else:

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, image_id, format=None):

        user = request.user

        image = self.find_own_image(image_id, user)

        if image is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        image.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeImage(APIView):

    def get(self, request, image_id, format=None):

        likes = Like.objects.filter(image__id=image_id)

        like_creators_ids = likes.values('creator__id')

        users = User.objects.filter(id__in=like_creators_ids)

        serializer = UserSerializer(users, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, image_id, format=None):

        user = request.user

        try:
            image = Image.objects.get(id=image_id)

        except Image.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            Like.objects.get(
                creator=user,
                image=image,
            )
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        except Like.DoesNotExist:
            Like.objects.create(
                creator=user,
                image=image,
            )
            # make notification
            return Response(status=status.HTTP_201_CREATED)


class UnLikeImage(APIView):

    def delete(self, request, image_id, format=None):

        user = request.user

        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            like = Like.objects.get(
                creator=user,
                image=image,
            )
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response(status=status.HTTP_304_NOT_MODIFIED)


class CommentOnImage(APIView):

    def post(self, request, image_id, format=None):

        user = request.user

        try:
            image = Image.objects.get(id=image_id)

        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(creator=user, image=image)
            # make notification
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class CommentDelete(APIView):

    def delete(self, request, comment_id, format=None):

        user = request.user

        try:
            comment = Comment.objects.get(id=comment_id, cretor=user)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Search(APIView):

    def get(self, request, format=None):
        hashtags = request.query_params.get('hashtags', None)

        if hashtags is not None:
            hashtags = hashtags.split(',')

            images = Image.objects.filter(tags__name__in=hashtags).distinct()

            serializer = CountImageSerializer(images, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ModerateComments(APIView):

    def delete(self, request, image_id, comment_id, format=None):

        user = request.user

        try:
            comment = Comment.objects.get(id=comment_id, image__id=image_id, image__creator=user)
            comment.delete()
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
