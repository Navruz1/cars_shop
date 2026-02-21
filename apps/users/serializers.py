from rest_framework import serializers
from .models import User

# GET List
class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'email', 'phone_number', 'role']
