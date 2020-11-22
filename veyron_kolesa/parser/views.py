# from requests import Response
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from veyron_kolesa.parser.serializers import ResultSerializer
from rest_framework import status, generics
from rest_framework.views import APIView


class ResultView(APIView):
  pass
