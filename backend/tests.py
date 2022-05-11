# from django.urls import reverse
# from rest_framework import status
from rest_framework.test import APITestCase
from .models import (Plant,
                     Family,
                     Genus,
                     Info,
                     SoilPreference,
                     UserPlant,
                     Edible)
from django.contrib.auth.models import User
# from backend.views import PlantViewSet
from backend.serializers import (PlantSerializer,
                                 FamilySerializer,
                                 GenusSerializer,
                                 InfoSerializer,
                                 SoilPreferenceSerializer,
                                 UserPlantSerializer,
                                 UserSerializer,
                                 EdibleSerializer)
import logging
from backend.generic_test_cases import (test_get_all,
                                        test_get_specific,
                                        test_create)

logger = logging.getLogger('testlogs')
title = logging.getLogger('title')


class TestCases(APITestCase):

    def setUp(self):
        # self.user_2 = User.objects.create(username='test-2')
        self.user_3 = User.objects.create_user(username='test-admin', is_staff=True)
        self.family_1 = Family.objects.create(
            family='Arecaceae2', family_description="test_description")
        self.genus_1 = Genus.objects.create(
            genus='Genusi', genus_description="test description")
        self.plant_1 = Plant.objects.create(
            plant_name='Foxtail Palm', plant_latin_name='Wodyetia bifurcata',
            plant_description='Test Description',
            family=self.family_1,
            genus=self.genus_1)
        self.info_1 = Info.objects.create(
            plant=self.plant_1, sun_preference=Info.SunPreferences.FULLSUN,
            climate=Info.Climates.TROPICAL, season=Info.Seasons.SUMMER,
            time_frame=Info.TimeFrames.DAILY,
            info_description='Test Description'
        )
        self.soilpreference_1 = SoilPreference.objects.create(
            plants=self.plant_1, preference=SoilPreference.SoilPreference.CLAY,
            soil_description='test description'
        )
        self.userplant_1 = UserPlant.objects.create(
            user=self.user_3, plant=self.plant_1
        )

        self.edible_1 = Edible.objects.create(
            plant=self.plant_1, is_fruit_edible=Edible.Edibility.NO,
            are_leaves_edible=Edible.Edibility.NO,
            are_roots_edible=Edible.Edibility.NO,
            are_flowers_edible=Edible.Edibility.NO,
            are_seeds_edible=Edible.Edibility.NO,
            edible_description='test description'
        )
        # Todo: create objects for each of the remaining models

    def test_plants(self):
        title.info('Starting Plant tests')
        test_get_all(self, Plant, PlantSerializer, 'plant-list')
        test_get_specific(self, 'plant-detail', self.plant_1, 'id')
        data1 = {
            "data": {
                "type": "Plant",
                "attributes": {
                    "plant_name": "scrout",
                    "plant_latin_name": "mcgoat",
                    "plant_description": "test description",
                    "family": "Arecaceae2",
                    "genus": "Genusi",
                }
            }
        }
        test_create(self, data1, 'plant-list', Plant, 'plant_name', 'scrout')

    def test_genus(self):
        title.info('Starting Genus tests')
        test_get_all(self, Genus, GenusSerializer, 'genus-list')
        test_get_specific(self, 'genus-detail', self.genus_1, 'genus')
        data1 = {
            "data": {
                "type": "Genus",
                "attributes": {
                    "genus": "Genusk",
                }
            }
        }
        test_create(self, data1, 'genus-list', Genus, 'genus_name', 'Genusk')

    def test_family(self):
        title.info('Starting Family tests')
        test_get_all(self, Family, FamilySerializer, 'family-list')
        test_get_specific(self, 'family-detail', self.family_1, 'family')
        data1 = {
            "data": {
                "type": "Family",
                "attributes": {
                    "family": "Moras"
                }
            }
        }
        test_create(self, data1, 'family-list', Family, 'family_name', 'Moras')

    def test_info(self):
        title.info('Starting Info tests')
        test_get_all(self, Info, InfoSerializer, 'info-list')
        test_get_specific(self, 'info-detail', self.info_1, 'id')
        data1 = {
            "data": {
                "type": "Info",
                "attributes": {
                    "sun_preference": "FS",
                    "climate": "T",
                    "season": "SP",
                    "time_frame": "AD",
                    "info_description": None,
                    "plant": "1",
                }
            }
        }
        test_create(self, data1, 'info-list', Info, 'sun_preference', 'FS')

    def test_soilpreference(self):
        title.info('Starting SoilPreference tests')
        test_get_all(self, SoilPreference, SoilPreferenceSerializer,
                     'soilpreference-list')
        test_get_specific(self, 'soilpreference-detail',
                          self.soilpreference_1, 'id')
        data1 = {
            "data": {
                "type": "SoilPreference",
                "attributes": {
                    "preference": "SA",
                    "soil_description": "placeholder soil info",
                    "plants": "1",
                }
            }
        }
        test_create(self, data1, 'soilpreference-list',
                    SoilPreference, 'soil_preference', 'SA')

    def test_userplant(self):
        title.info('Starting UserPlant tests')
        test_get_all(self, UserPlant, UserPlantSerializer, 'userplant-list')
        test_get_specific(self, 'userplant-detail', self.userplant_1, 'id')
        data1 = {
            "data": {
                "type": "UserPlant",
                "attributes": {
                    "user": 1,
                    "plant": 1,
                }
            }
        }
        test_create(self, data1, 'userplant-list',
                    UserPlant, 'username', 'test-2')

    def test_user(self):
        title.info('Starting User tests')
        test_get_all(self, User, UserSerializer, 'users-list')
        test_get_specific(self, 'users-detail', self.user_3, 'username')
        data1 = {
            "data": {
                "type": "User",
                "attributes": {
                    "username": "trhod17",
                    "is_staff": True,
                    "password": "W3terh0rse",
                }
            }
        }
        test_create(self, data1, 'users-list',
                    User, 'username', 'trhod17')

    def test_edible(self):
        title.info('Starting Edible tests')
        test_get_all(self, Edible, EdibleSerializer, 'edible-list')
        test_get_specific(self, 'edible-detail', self.edible_1, 'id')
        data1 = {
            "data": {
                "type": "Edible",
                "attributes": {
                    "is_fruit_edible": "N",
                    "are_leaves_edible": "N",
                    "are_roots_edible": "N",
                    "are_flowers_edible": "N",
                    "are_seeds_edible": "N",
                    "edible_description": "not edible",
                    "plant": "1",
                }
            }
        }
        test_create(self, data1, 'edible-list',
                    Edible, 'is_fruit_edible', 'N')
