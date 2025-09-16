from django.urls import path
from . import views

urlpatterns = [
    path('my-view/', views.my_view, name='my_view'),
    path('check-health/', views.check_heath, name='check_health'),
    path('burn-cpu/', views.cpu_burn, name='burn_cpu'),
    path('get_news_image/', views.get_image_urls, name='get_news_image'),
]
