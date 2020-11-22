from rest_framework import serializers
from veyron_kolesa.parser.models import Result
from veyron_kolesa.utils.utils import ChoiceValueDisplayField


class ResultSerializer(serializers.ModelSerializer):
    category = ChoiceValueDisplayField()
    class Meta:
        model = Result
        fields = '__all__'
