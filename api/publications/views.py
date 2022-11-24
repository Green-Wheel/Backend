from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.users.permissions import Check_API_KEY_Auth, SessionAuth
from api.chargers.models import PrivateChargers
from api.publications.models import Publication
from api.publications.serializers import OccupationRangeSerializer,PublicationSerializer
from api.publications.services import create_occupation, get_occupation_by_month, delete_occupation, update_occupation, \
    get_ocupation_by_id,upload_images
from api.users.permissions import Check_API_KEY_Auth



# Create your views here.
class PublicationOccupationApiView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]
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
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]
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
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]
    def get(self, request, publication_id, year, month, day=None):
        try:
            occupations = get_occupation_by_month(publication_id, year,month,day)
            return Response(occupations, status=status.HTTP_200_OK)
        except Publication.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# Create your views here.
class UploadPublicationImageApiView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]

    def post(self, request, publication_id):
        try:
            publication = upload_images(publication_id, request.FILES.getlist('file'), request.user.id)
            return Response(PublicationSerializer(publication).data, status=status.HTTP_200_OK)
        except Publication.DoesNotExist:
            return Response({"res": "Error: the publication with id " + str(publication_id) + "does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
