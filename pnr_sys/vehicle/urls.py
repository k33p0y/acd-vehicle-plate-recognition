from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='vehicle-landing'),
    path('home/', views.home, name='vehicle-home'),
    path('test/', views.test, name='vehicle-test'),
    # path('history/', views.history, name='vehicle-history'),
    path('history/', views.history_list, name='vehicle-history'), # history list page
    path('history-list/json/', views.history_list_json, name='vehicle-history-json'), # history list JSON
    path('signup/', views.signup, name='vehicle-signup'),
    # path('reports/', views.reports, name='vehicle-reports'),
    path('reports/', views.reports, name='vehicle-reports'),
]