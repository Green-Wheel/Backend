from rest_framework.views import APIView
from . import requests_api
from api.chargers.models import PublicChargers, Chargers, PrivateChargers


# Create your views here.
class ChargersView(APIView):
    def set_if_not_none(self, mapping, key, value):
        if value is not None:
            mapping[key] = value

    def get(self, request):
        # Agafar de la base de dades
        filters = {}
        type = request.GET.get('type')
        # town = request.GET.get('town')
        # self.set_if_not_none(filters, 'town', town)
        # self.set_if_not_none(filters, 'speed', speed)
        # self.set_if_not_none(filters, 'charger_type', charger_type)
        #
        if type == "public":
            chargers = PublicChargers.objects.filter(**filters)
        elif type == "private":
            chargers = PrivateChargers.objects.filter(**filters)
        else:
            chargers = Chargers.objects.filter(**filters)

        #requests_api.save_chargers_to_db()
