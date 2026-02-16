from django.urls import path
from .views_api import CarListAPI, CarCreateAPI, CarDetailAPI, CarUpdateAPI, CarDeleteAPI

urlpatterns = [
    path('', CarListAPI.as_view(), name='car-list'),
    path('create/', CarCreateAPI.as_view(), name='car-create'),
    path('<int:car_id>/', CarDetailAPI.as_view(), name='car-detail'),
    path('<int:car_id>/update/', CarUpdateAPI.as_view(), name='car_update'),
    path('<int:car_id>/delete/', CarDeleteAPI.as_view(), name='car_delete'),
]
