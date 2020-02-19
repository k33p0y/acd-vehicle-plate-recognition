from django.urls import path
from . import views

urlpatterns = [
    path('check-camera/', views.check_camera, name='api-check-camera'),
    path('check-captured/', views.check_captured, name='api-check-captured'),
    path('live-feed/', views.live_feed, name='api-live-feed'),
    path('live-feed-old/', views.live_feed_old, name='api-live-feed-old'),

    path('inout-partial/', views.inout_partial, name='api-inout-partial'),
    path('list-partial/', views.list_partial, name='api-list-partial'),
    # path('report/', views.report, name='api-report'),
    path('park-inout', views.park_inout, name='api-park-inout'),
    path('manual-input', views.manual_input, name='api-manual-input'),
    path('log-info/<int:log_id>/', views.log_info, name='api-log-info'),
    path('update-vehicle/<int:vehicle_id>/', views.update_vehicle, name='api-update-vehicle'),
]