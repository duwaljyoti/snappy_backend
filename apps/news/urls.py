from django.urls import path
from . import views

urlpatterns = [
    path('my-view/', views.my_view, name='my_view'),
    path('check-health/', views.check_heath, name='check_health'),
]
