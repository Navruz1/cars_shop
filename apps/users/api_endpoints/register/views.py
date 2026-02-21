from rest_framework.generics import CreateAPIView
from apps.users.models import User
from .serializers import RegisterSerializer

class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

__all__ = ['RegisterAPIView']  # При "import *" импортировать только RegisterAPIView
