from rest_framework import serializers

from veyron_kolesa.microservices.models import Service


class MicroServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
