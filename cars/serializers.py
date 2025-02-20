from rest_framework import serializers
from .models import AucCarsJapan, AucCarsChina, AucCarsKorea


class AucCarsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    year = serializers.IntegerField()
    price = serializers.IntegerField()
    brand = serializers.CharField()
    country = serializers.CharField()

    # @staticmethod
    # def get_country(instance) -> str:
    #     if isinstance(instance, AucCarsJapan):
    #         return "Japan"
    #     elif isinstance(instance, AucCarsChina):
    #         return "China"
    #     elif isinstance(instance, AucCarsKorea):
    #         return "Korea"
    #     return "Unknown"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["country"] = self.get_country(instance)
        return data
