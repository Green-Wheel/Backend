from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import requests_api
from api.chargers.models import PublicChargers, Chargers, PrivateChargers
from .serializers import PublicChargerSerializer


# Create your views here.
class ChargersView(APIView):
    def set_if_not_none(self, mapping, key, value):
        if value is not None:
            mapping[key] = value

    def get(self, request):
        # Agafar de la base de dades
        requests_api.save_chargers_to_db()
        filters = {}
        charger_type = request.GET.get('charger_type')
        # town = request.GET.get('town')
        # self.set_if_not_none(filters, 'town', town)
        # self.set_if_not_none(filters, 'speed', speed)
        self.set_if_not_none(filters, 'charger_type', charger_type)

        if charger_type == "public":
            chargers = PublicChargers.objects.filter(**filters)
        elif charger_type == "private":
            chargers = PrivateChargers.objects.filter(**filters)
        else:
            chargers = Chargers.objects.filter(**filters)

        charger_serializer = PublicChargerSerializer(chargers, many=True)
        return Response(charger_serializer.data, status=status.HTTP_200_OK)