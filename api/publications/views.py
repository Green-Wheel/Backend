from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.publications.models import Publication
from api.publications.serializers import PublicationSerializer
from api.publications.services import upload_images
from api.users.permissions import Check_API_KEY_Auth


# Create your views here.
class UploadPublicationImageApiView(APIView):
    permission_classes = [Check_API_KEY_Auth]
    authentication_classes = ()

    def post(self, request, publication_id):
        try:
            publication = upload_images(publication_id, request.FILES, request.user.id)
            return Response(PublicationSerializer(publication).data, status=status.HTTP_200_OK)
        except Publication.DoesNotExist:
            return Response({"res": "Error: the publication with id " + str(publication_id) + "does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
