import datetime
from abc import ABC

from django.contrib.auth.models import User
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from referenceBook.models import TelephoneNumber


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'password', 'username', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class TelephoneNumberSerializer(serializers.ModelSerializer):
    owner_username = serializers.StringRelatedField(source='owner')

    class Meta:
        model = TelephoneNumber
        fields = ['id', 'owner', 'owner_username', 'number']
        read_only_fields = ['id']

    def create(self, validated_data):
        telephoneNumber = TelephoneNumber.objects.create(owner=validated_data["owner"],
                                           number=validated_data['number'])
        return telephoneNumber
