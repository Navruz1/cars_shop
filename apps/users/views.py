from .models import User
from .serializers import UserCreateSerializer, UsersListSerializer
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)

# CREATE
class UserCrateAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

# GET List
class UsersListAPI(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersListSerializer