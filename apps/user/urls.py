from django.urls import path, include
from apps.user.views import user
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'users', views.user.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
