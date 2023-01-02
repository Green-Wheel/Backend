from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.reports.serializers import ReportReasonSerializer
from api.reports.services import create_rating_report, create_publication_report, create_user_report, get_report_reasons
from api.users.permissions import SessionAuth, Check_API_KEY_Auth


# Create your views here.
class ReportRatingApiView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]

    def post(self, request, rating_id):
        try:
            create_rating_report(rating_id, request.data, request.user.id)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReportPublicationApiView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]

    def post(self, request, publication_id):
        try:
            create_publication_report(publication_id, request.data, request.user.id)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReportUserApiView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]

    def post(self, request, reported_user):
        try:
            create_user_report(reported_user, request.data, request.user.id)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReportReasonsApiView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]

    def get(self, request):
        reasons = get_report_reasons()
        return Response(ReportReasonSerializer(reasons,many=True).data,status=status.HTTP_200_OK)