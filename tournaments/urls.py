from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
    path('', views.tournament_list, name='list'),
    path('new/', views.tournament_create, name='create'),
    path('<int:pk>/', views.tournament_detail, name='detail'),
    path('<int:pk>/register/', views.tournament_register, name='register'),
]
