from csv import field_size_limit
from rest_framework import serializers
from .models import Mobiles

class MobSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mobiles
        fields='__all__'