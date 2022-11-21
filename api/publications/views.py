from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.chargers.models import PrivateChargers
from api.publications.models import Publication
from api.publications.serializers import OccupationRangeSerializer
from api.publications.services import create_occupation, get_occupation_by_month, delete_occupation, update_occupation, \
    get_ocupation_by_id


# Create your views here.
class PublicationOccupationApiView(APIView):
    def post(self, request,publication_id):
        try:
            new_occupations = create_occupation(request.data, request.user.id, publication_id)
            # add charger to user
            return Response(new_occupations, status=status.HTTP_200_OK)
        except Publication.DoesNotExist:
            return Response({"res": "Publication does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ConcretePublicationOccupationApiView(APIView):
    def get(self, request, publication_id, occupation_id):
        try:
            occupation = get_ocupation_by_id(occupation_id)
            return Response(OccupationRangeSerializer(occupation).data, status=status.HTTP_200_OK)
        except Publication.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, publication_id, occupation_id):
        try:
            occupation = update_occupation(occupation_id, request.data,request.user.id)
            return Response(OccupationRangeSerializer(occupation).data, status=status.HTTP_200_OK)
        except Publication.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, publication_id, occupation_id):
        try:
            delete_occupation(occupation_id,request.user.id,)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_404_NOT_FOUND)


class MonthPublicationOccupation(APIView):
    def get(self, request, publication_id, year, month):
        try:
            occupations = get_occupation_by_month(publication_id, year,month)
            return Response(occupations, status=status.HTTP_200_OK)
        except Publication.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
