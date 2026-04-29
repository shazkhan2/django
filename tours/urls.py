from django.urls import path
from . import views

app_name = 'tours'

urlpatterns = [
    path('', views.index, name='index'),
    path('dispatcher/', views.dispatcher_dashboard, name='dispatcher_dashboard'),
    path('driver/', views.driver_dashboard, name='driver_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create/', views.create_tour, name='create_tour'),
    path('assign/<int:tour_id>/', views.assign_driver, name='assign_driver'),
    path('driver/complete/<int:tour_id>/', views.complete_tour, name='complete_tour'),
]
