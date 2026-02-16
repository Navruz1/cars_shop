from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend # pip install django-filter
from .models import Car
from .serializers import CarSerializer

# Create your views here.

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['manufacturer', 'year', 'mileage']
    search_fields = ['name', 'manufacturer']
    ordering_fields = ['price', 'year', 'name', 'mileage']
    ordering = ['name']
    