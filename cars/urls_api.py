from django.urls import path
from .views_api import (
    CarListAPI,
    CarCreateAPI,
    CarDetailAPI,
    CarUpdateAPI,
    CarDeleteAPI,
    CarImageCreateAPI,
    CarImagesGetAPI
)

urlpatterns = [
    path('', CarListAPI.as_view(), name='car-list'),                            # GET (List)
    path('create/', CarCreateAPI.as_view(), name='car-create'),                 # POST
    path('<int:id>/', CarDetailAPI.as_view(), name='car-detail'),               # GET (Detail)
    path('<int:id>/update/', CarUpdateAPI.as_view(), name='car-full-update'),   # PUT и PATH
    path('<int:id>/delete/', CarDeleteAPI.as_view(), name='car-delete'),        # DELETE
    path('<int:id>/images/', CarImageCreateAPI.as_view(), name='car-images-create'),
    path('images/', CarImagesGetAPI.as_view(), name='cars-images-get')
]
