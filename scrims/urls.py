from django.urls import path
from . import views

app_name = 'scrims'

urlpatterns = [
    path('', views.scrim_list, name='list'),
    path('new/', views.scrim_create, name='create'),
    path('<int:pk>/accept/', views.scrim_accept, name='accept'),
    path('<int:pk>/report/', views.scrim_report, name='report'),
]
