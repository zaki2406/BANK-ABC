# your_app/serializers.py
from rest_framework import serializers

class FinancialDataSerializer(serializers.Serializer):
    file = serializers.FileField()
