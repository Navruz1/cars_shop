from .models import User
from .serializers import UsersListSerializer
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)

# GET List
class UsersListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersListSerializer