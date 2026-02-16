import django_filters
from .models import Car

class CarFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    manufacturer = django_filters.CharFilter(
        field_name='manufacturer',
        lookup_expr='icontains'
    )
    # Диапазонные фильтры
    year_from = django_filters.NumberFilter(
        field_name='year', lookup_expr='gte'
    )
    year_to = django_filters.NumberFilter(
        field_name='year', lookup_expr='lte'
    )

    price_from = django_filters.NumberFilter(
        field_name='price', lookup_expr='gte'
    )
    price_to = django_filters.NumberFilter(
        field_name='price', lookup_expr='lte'
    )

    mileage_from = django_filters.NumberFilter(
        field_name='mileage', lookup_expr='gte'
    )
    mileage_to = django_filters.NumberFilter(
        field_name='mileage', lookup_expr='lte'
    )

    class Meta:
        model = Car
        fields = [
            'name',
            'manufacturer',
            'year_from', 'year_to',
            'price_from', 'price_to',
            'mileage_from', 'mileage_to',
        ]