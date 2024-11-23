from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import  views
from .views import PortalView

router = DefaultRouter()
router.register(r'portals', views.PortalView, basename='portal')

urlpatterns = [
    path('', include(router.urls)),
]

