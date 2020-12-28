from rest_auth.utils import import_callable
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.conf import settings

from images.serializers import CountImageSerializer
from .models import User

# accounts.authentication 파일을 만들어서 django,contrib.auth의 get_user_model 메서드를 직접 정의한 후
# 마지막에 북마크한 페이지의 방법 대로 authentication을 작성해보자.


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'profile_image',
            'username',
        )


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER # 이 중 임포스터가 있다(아마도).
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER #

        payload = jwt_payload_handler(obj) #
        token = jwt_encode_handler(payload) #

        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token','pk','username','email','password','profile_image')


from rest_auth.serializers import JWTSerializer


class CustomJWTSerializer(JWTSerializer):
    """
    Serializer for JWT authentication.
    """
    token = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        """
        Required to allow using custom USER_DETAILS_SERIALIZER in
        JWTSerializer. Defining it here to avoid circular imports
        """
        rest_auth_serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})
        JWTUserDetailsSerializer = import_callable(
            rest_auth_serializers.get('USER_DETAILS_SERIALIZER', UserSerializer) # 여기도 임포스터가 있는 듯 하다
        )
        user_data = JWTUserDetailsSerializer(obj['user'], context=self.context).data
        return user_data


class UserProfileSerializer(serializers.ModelSerializer):
    images = CountImageSerializer(many=True, read_only=True)

    post_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            'profile_image',
            'username',
            'post_count',
            'followers_count',
            'following_count',
            'images',
        )
