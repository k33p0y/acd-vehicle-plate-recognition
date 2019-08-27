from django.urls import path
from . import views

urlpatterns = [
    path('check-camera/', views.check_camera, name='api-check-camera'),
    path('check-captured/', views.check_captured, name='api-check-captured'),
    path('live-feed/', views.live_feed, name='api-live-feed'),
]