from rest_framework import serializers

"""
class NameSerializer(serializers.ModelSerializer):
    class Meta:
        model = "pass"
        fields = []
"""

class ChargersTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargersType
        fields = ["id", "name", "current_id", "type_vehicle_id"]