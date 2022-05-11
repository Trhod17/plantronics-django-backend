from rest_framework import serializers
from django.contrib.auth.models import User, Group
from backend.models import (Plant,
                            Family,
                            Genus,
                            Info,
                            UserPlant,
                            SoilPreference,
                            Edible)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        lookup_field = 'username'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        lookup_field = 'name'


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'


class GenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genus
        fields = '__all__'


class InfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Info
        fields = '__all__'


class SoilPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilPreference
        fields = '__all__'


class UserPlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlant
        fields = '__all__'
        lookup_field = 'user'


class EdibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edible
        fields = '__all__'
