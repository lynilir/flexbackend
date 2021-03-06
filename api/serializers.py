from rest_framework import serializers
from api.models import Restaurant, Like, Dislike
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'place_id', 'lat', 'lng', 'user_likes',
        'user_dislikes', 'address', 'phone_number', 'image_url')

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', 'restaurant')

class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ('user', 'restaurant')

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        write_only=True
    )

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'write_only': True},
        }
