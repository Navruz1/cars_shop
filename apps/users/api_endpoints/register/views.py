from rest_framework.generics import CreateAPIView
from apps.users.models import User

from .serializers import RegisterSerializer

class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

