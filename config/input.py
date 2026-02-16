# config/input.py
import os
import django

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from cars.models import Car

# Список автомобилей
cars_data = [
    {"name": "Corolla", "manufacturer": "Toyota", "year": 2020, "price": 15000.00, "mileage": 35000},
    {"name": "Civic", "manufacturer": "Honda", "year": 2019, "price": 14000.00, "mileage": 42000},
    {"name": "Model 3", "manufacturer": "Tesla", "year": 2021, "price": 35000.00, "mileage": 15000},
    {"name": "Mustang", "manufacturer": "Ford", "year": 2018, "price": 27000.00, "mileage": 50000},
    {"name": "Camry", "manufacturer": "Toyota", "year": 2022, "price": 28000.00, "mileage": 10000},
    {"name": "Accord", "manufacturer": "Honda", "year": 2020, "price": 22000.00, "mileage": 30000},
    {"name": "X5", "manufacturer": "BMW", "year": 2019, "price": 45000.00, "mileage": 40000},
    {"name": "A4", "manufacturer": "Audi", "year": 2021, "price": 37000.00, "mileage": 20000},
    {"name": "Golf", "manufacturer": "Volkswagen", "year": 2018, "price": 18000.00, "mileage": 55000},
    {"name": "Altima", "manufacturer": "Nissan", "year": 2020, "price": 20000.00, "mileage": 25000},
]

# Добавление автомобилей в базу
for car in cars_data:
    Car.objects.create(**car)

print("10 автомобилей успешно добавлены!")
