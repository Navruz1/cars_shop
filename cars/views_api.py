from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import Car
from .serializers import CarSerializer
from .filters import CarFilter
from .utils import api_response

# Просмотр списка машин
# class CarListAPI(APIView):
#     def get(self, request):
#         cars = Car.objects.all()
#         serializer = CarSerializer(cars, many=True)
#         return api_response(data=serializer.data)
class CarListAPI(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter

# Создать машину
class CarCreateAPI(APIView):
    def post(self, request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data, status_code=201)
        return api_response(data=serializer.errors, status_code=400)

# Детали одной машины
class CarDetailAPI(APIView):
    def get(self, request, car_id):
        try:
            car = Car.objects.get(pk=car_id)
            serializer = CarSerializer(car)
            return api_response(data=serializer.data)
        except Car.DoesNotExist:
            return api_response(data=None, message="Car not found", status_code=404)

# Обновление данных одной машины
class CarUpdateAPI(APIView):
    def put(self, request, car_id):
        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return api_response({"detail": "Car not found"}, status_code=404)

        serializer = CarSerializer(car, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data)
        return api_response(data=serializer.errors, status_code=400)

# Удаление машины
class CarDeleteAPI(APIView):
    def delete(self, request, car_id):
        try:
            car = Car.objects.get(id=car_id)
            car.delete()
            return api_response({"detail": "Car deleted"}, status_code=204)
        except Car.DoesNotExist:
            return api_response({"detail": "Car not found"}, status_code=404)

