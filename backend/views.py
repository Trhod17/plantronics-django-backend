from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from backend.serializers import (PlantSerializer,
                                 UserSerializer,
                                 GroupSerializer,
                                 FamilySerializer,
                                 GenusSerializer,
                                 InfoSerializer,
                                 SoilPreferenceSerializer,
                                 UserPlantSerializer,
                                 EdibleSerializer)

from backend.models import (Plant,
                            Family,
                            Genus,
                            Info,
                            SoilPreference,
                            UserPlant,
                            Edible)
from django.db import IntegrityError
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import django_filters
from django.shortcuts import render
import json
from rest_framework.decorators import api_view
import cloudinary


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)  # data is a dictionary
            user = User.objects.create_user(
                username=data['username'],
                password=data['password'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'])

            user.save()

            group = Group.objects.get(name='site_user')
            user.groups.add(group)

            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
        except IntegrityError:
            return JsonResponse(
                {'error': 'username and/or email taken. choose another username and/or email'},
                status=400)
    else:
        return JsonResponse({'message': 'get request not supported on this url'}, status=404)


@csrf_exempt
def login(request):
    if request.method == 'POST':

        data = JSONParser().parse(request)
        user = authenticate(
            request,
            username=data['username'],
            password=data['password'])
        if user is None:
            return JsonResponse(
                {'error': 'unable to login. check username and password'},
                status=400)
        else:  # return user token
            try:
                token = Token.objects.get(user=user)
            except:  # if token not in db, create a new one
                token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
    else:
        return JsonResponse({'message': 'get request not supported on this url'}, status=404)


@ csrf_exempt
def user(request):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = User.objects.filter(username=data['user']).exists()
        if user == False:
            return JsonResponse({'user': 'user not found'}, status=200)
        else:
            return JsonResponse({'user': 'username taken'}, status=302)

    return JsonResponse({'message': 'get request not supported on this url'}, status=404)


@csrf_exempt
def plantInfo(request):
    if (request.method == 'POST'):
        data = JSONParser().parse(request)

        get = Info.objects.filter(
            plant__pk=data['id']).values('id', 'plant__plant_name', 'season', 'time_frame', 'climate', 'sun_preference', 'info_description', 'created_by__username')

        json_object = json.loads(json.dumps(list(get)))

        if get:

            for x in json_object:
                x['season'] = Info.Seasons(x['season']).label
                x['time_frame'] = Info.TimeFrames(x['time_frame']).label
                x['climate'] = Info.Climates(x['climate']).label
                x['sun_preference'] = Info.SunPreferences(
                    x['sun_preference']).label

            return JsonResponse({'info': json_object}, status=200)
        else:
            return JsonResponse({"Error": "this plant has no info"}, status=404)
    else:
        return JsonResponse({'message': 'get request not supported on this url'}, status=404)


@csrf_exempt
def plantSoil(request):
    if (request.method == 'POST'):
        data = JSONParser().parse(request)

        get = SoilPreference.objects.filter(
            plants__pk=data['id']).values('id', 'plants__plant_name', 'preference', 'soil_description', 'created_by__username')

        json_object = json.loads(json.dumps(list(get)))

        if get:

            for x in json_object:
                x['preference'] = SoilPreference.SoilPreference(
                    x['preference']).label

            return JsonResponse({'soil': json_object}, status=200)
        else:
            return JsonResponse({"Error": "this plant has no soil preference data"}, status=404)
    else:
        return JsonResponse({'message': 'get request not supported on this url'}, status=404)


@csrf_exempt
def plantEdibles(request):
    if (request.method == 'POST'):
        data = JSONParser().parse(request)

        get = Edible.objects.filter(
            plant__pk=data['id']).values('id', 'plant__plant_name', 'is_fruit_edible', 'are_leaves_edible',
                                         'are_roots_edible', 'are_seeds_edible', 'are_flowers_edible', 'fruit_image', 'flower_image',
                                         'seed_image', 'root_image', 'leaf_image', 'edible_description', 'created_by__username')

        json_object = json.loads(json.dumps(list(get)))

        if get:

            for x in json_object:
                x['is_fruit_edible'] = Edible.Edibility(
                    x['is_fruit_edible']).label
                x['are_leaves_edible'] = Edible.Edibility(
                    x['are_leaves_edible']).label
                x['are_roots_edible'] = Edible.Edibility(
                    x['are_roots_edible']).label
                x['are_seeds_edible'] = Edible.Edibility(
                    x['are_seeds_edible']).label
                x['are_flowers_edible'] = Edible.Edibility(
                    x['are_flowers_edible']).label

                # x['fruit_image'] = cloudinary.CloudinaryImage(
                #     x['fruit_image']).build_url()

            return JsonResponse({'edible': json_object}, status=200)
        else:
            return JsonResponse({"Error": "this plant has no ediblity data"}, status=404)
    else:
        return JsonResponse({'message': 'get request not supported on this url'}, status=404)


@csrf_exempt
def getPlants(request):
    if (request.method == 'GET'):

        get = Plant.objects.all().values('id', 'plant_name', 'plant_latin_name',
                                               'plant_image', 'plant_description', 'family', 'genus', 'created_by__username')

        json_object = json.loads(json.dumps(list(get)))

        return JsonResponse({'plants': json_object}, status=200)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        get = Plant.objects.filter(
            id=data['id']).values('plant_name', 'plant_latin_name',
                                               'plant_image', 'plant_description', 'family', 'genus', 'created_by__username')
        json_object = json.loads(json.dumps(list(get)))

        return JsonResponse({'plants': json_object}, status=200)
    else:
        return JsonResponse({'message': 'request not supported on this url'}, status=404)


@csrf_exempt
def myPlants(request):
    if (request.method == 'GET'):
        get = UserPlant.objects.all().values('user__username', 'plant__plant_name')
        json_object = json.loads(json.dumps(list(get)))

        return JsonResponse({'userplants': json_object}, status=200)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'username'


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class PlantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'plant_name'


class FamilyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class GenusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Genus.objects.all()
    serializer_class = GenusSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class InfoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'plant'


class SoilPreferenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SoilPreference.objects.all()
    serializer_class = SoilPreferenceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class UserPlantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = UserPlant.objects.all()
    serializer_class = UserPlantSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class EdibleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Edible.objects.all()
    serializer_class = EdibleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
