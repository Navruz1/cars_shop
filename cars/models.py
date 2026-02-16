from django.db import models

# Create your models here.

class Car(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.PositiveIntegerField(help_text="Пробег автомобиля в км")

    def __str__(self):
        return f"{self.manufacturer} {self.name} ({self.year})"