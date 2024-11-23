from django.contrib.auth.models import User
from rest_framework import viewsets

from apps.user.models import UserPortal
from apps.user.serializers import user
from apps.user.serializers.user import UserPortalSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = user.UserSerializer

class UserPortalViewSet(viewsets.ModelViewSet):
    queryset = UserPortal.objects.all()
    serializer_class = UserPortalSerializer
