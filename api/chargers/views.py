from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import requests_api
from api.chargers.models import PublicChargers, Chargers, PrivateChargers, Localizations, Town, Publication
from api.chargers.serializers import PublicChargerSerializer, ChargerSerializer, privateChargerSerializer, PublicationSerializer
from api.chargers.utils import get_localization, get_speed, get_connection, get_current, get_town

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

class AddChargerView(APIView):
    def post(self, request):
        localization = get_localization(request.data["Latitude"], request.data["Longitude"])
        speed_type = get_speed(request.data["velocity"])
        connection_type = get_connection(request.data["tipusCarregador"])
        current_type = get_current('AC')
        town = get_town("Barcelona", "Barcelona")

        try:
            # publication = Publication(title=request.data['title'],
            #                           description=request.data['description'],
            #                           direction="directon de prueva",
            #                           town=town,
            #                           localization=localization)
            # publication.save()
            #
            # charger = Chargers(publication_ptr_id=publication.id,
            #                    power=request.data["power"])
            # charger.save()
            # charger.speed.set([speed_type])
            # charger.connection_type.set([connection_type])
            # charger.current_type.set([current_type])

            private = PrivateChargers(title=request.data['title'],
                                      description=request.data['description'],
                                      direction="directon de prueva",
                                      town=town,
                                      localization=localization,
                                      power=request.data["power"],
                                      price=request.data["price"])
            private.save()
            private.speed.set([speed_type])
            private.connection_type.set([connection_type])
            private.current_type.set([current_type])
            private_serializaer = privateChargerSerializer(private, many=False)
            return Response({"res": "Charger added", "data":private_serializaer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        types = ChargersType.objects.all()
        serializer = ChargersTypeSerializer(types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        #match request.data["action"]:
        #    case "chargerType":
        #        return self.get_chargers_types()
        #    case "typeSpeed":
        #        return self.get_types_speeds()
        #    case _:
        #        return Response({"res": "Action not found"}, status=status.HTTP_400_BAD_REQUEST)