from django.urls import path
from . import views

urlpatterns = [
    path('get-image/', views.get_image, name='api-get-image'),
    path('check-captured/', views.check_captured, name='api-check-captured'),
    path('live-feed/', views.live_feed, name='api-live-feed'),
]