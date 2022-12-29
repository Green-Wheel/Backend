from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.users.permissions import Check_API_KEY_Auth, SessionAuth
from api.vehicles.models import CarsModel, Cars, CarsBrand
from api.vehicles.serializers import CarsModelSerializer, CarsSerializer, CarsBrandSerializer, \
    CarsBrandYearSerializer, CarsDetailedSerializer
from api.vehicles.services import create_car, get_models_by_brand_id, get_years_of_model, \
    get_car_by_id, update_car, delete_car, get_brands, get_filtered_vehicles, select_car


# Create your views here.
class VehiclesView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]

    def get(self, request):
        cars = get_filtered_vehicles(request.query_params, request.user.id)
        serializer = CarsSerializer(cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            new_car = create_car(request.data, request.user.id)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(CarsDetailedSerializer(new_car).data, status=status.HTTP_200_OK)
            else:
                return Response(CarsDetailedSerializer(new_car).data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DetailedVehicleView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]
    def get(self, request, car_id):
        try:
            car = get_car_by_id(car_id)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(CarsDetailedSerializer(car).data, status=status.HTTP_200_OK)
            else:
                return Response(CarsDetailedSerializer(car).data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        except Cars.DoesNotExist:
            return Response({"res": "Car not found"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, car_id):
        try:
            car = update_car(car_id, request.data, request.user.id)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(CarsDetailedSerializer(car).data, status=status.HTTP_200_OK)
            else:
                return Response(CarsDetailedSerializer(car).data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, car_id):
        try:
            delete_car(car_id, request.user.id)
            return Response({"res": "Car deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Cars.DoesNotExist:
            return Response({"res": "Car not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BrandsView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]
    def get(self, request):
        try:
            brands = get_brands()
            serializer = CarsBrandSerializer(brands, many=True)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ModelsBrandView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]
    def get(self, request, brand_id):
        try:
            models = get_models_by_brand_id(brand_id)
            serializer = CarsModelSerializer(models, many=True)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')
        except CarsModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ModelsBrandYearView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]
    def get(self, request, brand_id, model_name):
        try:
            years = get_years_of_model(brand_id, model_name)
            print(years)
            serializer = CarsBrandYearSerializer(years, many=True)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SelectVehicleView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]
    def put(self, request, car_id):
        try:
            select_car(car_id, request.user.id)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)