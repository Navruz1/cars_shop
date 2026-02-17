from rest_framework import serializers
from .models import Car, CarImage


# CREATE

class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['name', 'manufacturer', 'year', 'price', 'mileage']


# GET (List)

class CarListSerializer(serializers.ModelSerializer):
    images_count = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['id', 'name', 'manufacturer', 'year', 'price', 'mileage', 'images_count']

    def get_images_count(self, obj):
        return obj.images.count()


# PUT и PATCH

class CarUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'name', 'manufacturer', 'year', 'price', 'mileage']


# CREATE (Add) Image

class CarImageSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField(source='get_image_url')

    class Meta:
        model = CarImage
        fields = ['id', 'image', 'image_url']


# GET (Images List)

class CarsImagesListSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField(source='get_image_url')

    class Meta:
        model = CarImage
        fields = ['id', 'car_id', 'image', 'image_url']


# GET (Car Details)

class CarDetailSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'name', 'manufacturer', 'year', 'price', 'mileage', 'images']