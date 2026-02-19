from django.db import models
# from drf_spectacular.utils import extend_schema_field
# from rest_framework import serializers

# Create your models here.

class Car(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.PositiveIntegerField(help_text="Пробег автомобиля в км")

    def __str__(self):
        return f"{self.manufacturer} {self.name} ({self.year})"


# Создаём отдельную модель чтобы к одной машине можно было привязать несколько изображений

class CarImage(models.Model):
    image = models.ImageField(upload_to="cars/")
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        verbose_name="Машина",
        related_name="images"
    )

    # @extend_schema_field(serializers.CharField())
    def get_image_url(self):
        return self.image.url if self.image else ""

    def __str__(self):
        return f"Image(s) of {self.car}"
