from rest_framework import serializers
from .models import Mobiles
from django.contrib.auth.models import User

class MobSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mobiles
        fields='__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True)  #temperary field

    class Meta:
        model=User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2', None)        #removing before saving to db
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)