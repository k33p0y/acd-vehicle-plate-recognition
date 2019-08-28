from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='vehicle-landing'),
    path('home/', views.home, name='vehicle-home'),
    path('test/', views.test, name='vehicle-test'),
]
