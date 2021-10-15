from rest_framework import serializers

from .models import TFinances


class FinancesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TFinances
        fields = '__all__'
