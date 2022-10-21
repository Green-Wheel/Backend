from rest_framework.views import APIView
from . import requests_api
from api.chargers.models import PublicChargers, Chargers, PrivateChargers

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
    def get_localization(self, localization_id):
        try:
            return Localizations.objects.get(id=localization_id)
        except Localizations.DoesNotExist:
            return None

    def get_charger_type(self, type_id):
        try:
            return ChargersType.objects.get(id=type_id)
        except ChargersType.DoesNotExist:
            return None

    def get_chargers_types(self):
        try:
            return ChargersType.objects.all()
        except ChargersType.DoesNotExist:
            return None
    def get_types_speeds(self):
        try:
            return TypeSpeed.objects.all()
        except TypeSpeed.DoesNotExist:
            return None
    def get_type_speed(self, type_id):
        try:
            return TypeSpeed.objects.get(id=type_id)
        except TypeSpeed.DoesNotExist:
            return None

    def post(self, request):
        localization = Localizations.objects.get(id=1)#request.data["localization"])
        speed_type = SpeedsType.objects.get(id=1)#request.data["speed_type"])
        connection_type = ConnectionsType.objects.get(id=1)#request.data["connection_type"])
        current_type = CurrentsType.objects.get(id=1)#request.data["current_type"])

        publication = PublicationSerializer(data={title: request.data["title"],
                                                  description: request.data["description"],
                                                  localization: localization})
        if publication.is_valid():
            charger = ChargersSerializer(data={publication_ptr_id: publication,
                                               connection_type_id: connection_type.id,
                                               current_type_id: current_type.id,
                                               speed_type_id: speed_type.id})
            if charger.is_valid():
                private_charger = PrivateChargersSerializer(data={charger_ptr_id: charger.id,
                                                                  price: request.data["price"]})
                if private_charger.is_valid():
                    publication.save()
                    charger.save()
                    private_charger.save()
                    return Response({"res": "Charger added"}, status=status.HTTP_201_CREATED)

        #try:
        data = {
            "title": request.data["title"],
            "description": request.data["description"],
        }
        publication = Publication(title=request.data['title'],
                                  description=request.data['description'],
                                  localization=Localizations.objects.get(id=1),)
        publication.save()

        charger = Chargers(publication_ptr_id=publication,
                           power=request.data["power"],
                           available=True)
        charger.save()

        private = PrivateChargers(charger_ptr_id=charger,
                                  price=request.data["price"])
        private.save()
        return Response({"res": "Charger added"}, status=status.HTTP_200_OK)
        #except Exception as e:
            #print(e)
            #return Response({"res": "Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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























