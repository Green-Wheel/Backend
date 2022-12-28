from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.vehicles.models import CarsModel, Cars
from api.vehicles.serializers import CarsModelSerializer, CarsSerializer
from api.vehicles.services import get_data_vehicles, create_car


# Create your views here.
class VehiclesView(APIView):
    def get(self, request):
        models = Cars.objects.all()
        serializer = CarsSerializer(models, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            new_car = create_car(request.data, request.user.id)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(CarsSerializer(new_car).data, status=status.HTTP_200_OK)
            else:
                return Response(CarsSerializer(new_car).data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VehiclesModelsView(APIView):
    def get(self, request):
        get_data_vehicles()
        models = CarsModel.objects.all()
        serializer = CarsModelSerializer(models, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
