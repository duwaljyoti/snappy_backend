from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

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
        logging_user = authenticate(username=request.data.get('username'), password=request.data.get('password'))

        if user:
            refresh = RefreshToken.for_user(logging_user)
            access = refresh.access_token

            return Response({
                'message': 'Login successful',
                'username': logging_user.username,
                'access': str(access),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
