from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Chargers


# Create your views here.
class ChargerInfoApiView(APIView):
    def get_charger(self, charger_id):
        try:
            return Chargers.objects.get(id=charger_id)
        except Chargers.DoesNotExist:
            return None

    # def get(self, request):
    # def put(self, request):


