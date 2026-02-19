from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer

class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer

# __all__ = ['register']  # Импортировать только register
