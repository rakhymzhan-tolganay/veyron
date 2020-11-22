from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from veyron_kolesa.microservices.models import Service
from veyron_kolesa.microservices.serializers import MicroServiceSerializer


class ServicesViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = MicroServiceSerializer
    queryset = Service.objects.all()
