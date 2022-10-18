from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Publication, Chargers, ChargersType, TypeSpeed, Localizations

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
        print("request.data")
        user_id = 1
        publication = Publication(title=request.data['title'],
                                  description=request.data['description'],
                                  latitude_id=1,
                                  longitude_id=1,
                                  price=request.data['price'])
        publication.save()
        charger = Chargers(publication_ptr_id=publication, power=request.data['power'], available=True,
                                          charger_type=self.get_charger_type(1), speed=self.get_type_speed(1))
        charger.save()
        return Response({"res": "Language changed"}, status=status.HTTP_200_OK)

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