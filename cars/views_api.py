from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from .models import Car, CarImage
from .filters import CarFilter
from .serializers import (
    CarCreateSerializer,
    CarListSerializer,
    CarDetailSerializer,
    CarUpdateSerializer,
    CarImageSerializer,
    CarsImagesListSerializer
)


# Просмотр списка машин

class CarListAPI(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter


# Создание машины

class CarCreateAPI(CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarCreateSerializer


# Детали одной машины

class CarDetailAPI(RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarDetailSerializer
    lookup_field = "id"


# Обновление данных машины

class CarUpdateAPI(UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarUpdateSerializer
    lookup_field = "id"


# Удаление машины

class CarDeleteAPI(DestroyAPIView):
    queryset = Car.objects.all()
    lookup_field = "id"


# Добавление изображений машины

class CarImageCreateAPI(CreateAPIView):
    serializer_class = CarImageSerializer

    def perform_create(self, serializer):
        car = get_object_or_404(Car, id=self.kwargs['id'])
        serializer.save(car=car)


# Вывод всех изображений

class CarImagesGetAPI(ListAPIView):
    queryset = CarImage.objects.all()
    serializer_class = CarsImagesListSerializer


