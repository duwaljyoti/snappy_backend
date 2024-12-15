from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from apps.user.models import UserPortal
from apps.user.serializers import user
from apps.user.serializers.user import UserPortalSerializer
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = user.UserSerializer

class UserPortalViewSet(viewsets.ModelViewSet):
    queryset = UserPortal.objects.all()
    serializer_class = UserPortalSerializer


class SignInView(APIView):
    def post(self, request):
        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))

        if user:
            return Response({
                'message': 'Login successful',
                'username': user.username
            }, status=status.HTTP_200_OK)

            # If authentication fails, return an error response
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
