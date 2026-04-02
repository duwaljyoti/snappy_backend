from django.urls import path
from . import views

urlpatterns = [
    path('my-view/', views.my_view, name='my_view'),
    path('check-health/', views.check_heath, name='check_health'),
    path('send-test-email/', views.send_test_mail, name='send_test_email'),
    path('burn-cpu/', views.cpu_burn, name='burn_cpu'),
    path('get_news_image/', views.get_image_urls, name='get_news_image'),
    path('stress/', views.stress_test_view, name='stress')
]
