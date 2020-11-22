from django.contrib.auth import get_user_model
import logging

from rest_framework import generics, viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from veyron_kolesa.users.serializers import NativeUserSerializer
from veyron_kolesa.utils.mixins import MultiSerializerViewSetMixin

logger = logging.getLogger(__name__)


User = get_user_model()


class UserListDebug(generics.ListAPIView):
    serializer_class = NativeUserSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    queryset = User.objects.all()
