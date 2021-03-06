# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from api.models import Restaurant, Like, Dislike
from api.serializers import RestaurantSerializer, LikeSerializer, DislikeSerializer, UserSerializer
from django.contrib.auth.models import User


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        # import pdb; pdb.set_trace()
        token = Token.objects.get(key=response.data['token'])
        status = response.status_code
        return Response({'token': token.key,
                         'username': token.user.username,
                         'user_id': token.user.id,
                         'status': status
                         })

@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def create_user(request):
    serialized = UserSerializer(data=request.data, context={'request': request})
    if serialized.is_valid():
        #new user
        user = User(
            username=request.data['username'],
            email=request.data['email'],
        )
        user.set_password(request.data['password'])
        user.save()
        serialized = UserSerializer(user)
        username = serialized.data['username']
        user_id = serialized.data['id']
        token, created = Token.objects.get_or_create(user=serialized.instance)
        return Response({'username': username,
                         'user_id': user_id,
                         'token': token.key,
                         'status': status.HTTP_201_CREATED},
        status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
def restaurant_list(request):
    """
    List all restaurants, or create a new restaurant.
    """
    if request.method == 'GET':
        restaurants = Restaurant.objects.all()

        # .015 lat/lng unit ~ 1 mile
        # north = float(request.GET['lat']) + .015
        # east = float(request.GET['lng']) + .015
        # south = float(request.GET['lat']) - .015
        # west = float(request.GET['lng']) - .015

        # location filtering
        # restaurants = Restaurant.objects.filter(
        #     lat__lte=north
        #     ).filter(
        #     lat__gte=south
        #     ).filter(
        #     lng__lte=east
        #     ).filter(
        #     lng__gte=west
        #     )

        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)


    elif request.method == 'POST':
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# Create your views here.

@api_view(['GET', 'PUT', 'DELETE'])
def restaurant_detail(request, pk):

    try:
        restaurant = Restaurant.objects.get(pk=pk)
    except Restaurant.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':

        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RestaurantSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        restaurant.delete()
        return HttpResponse(status=204)

@api_view(['POST'])
def create_like(request):

    dislike_list = Dislike.objects.filter(user=request.data['user']).filter(restaurant=request.data['restaurant'])
    for dislike in dislike_list:
        dislike.delete()

    if request.method == 'POST':
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def create_dislike(request):
    like_list = Like.objects.filter(user=request.data['user']).filter(restaurant=request.data['restaurant'])
    for like in like_list:
        like.delete()

    if request.method == 'POST':
        serializer = DislikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
