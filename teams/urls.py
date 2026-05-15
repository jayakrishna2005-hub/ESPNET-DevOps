from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.team_list, name='list'),
    path('new/', views.team_create, name='create'),
    path('<int:pk>/', views.team_detail, name='detail'),
    path('<int:pk>/dashboard/', views.team_dashboard, name='dashboard'),
    path('<int:pk>/recruit/', views.create_recruitment_post, name='create_recruitment'),
    path('apply/<int:post_id>/', views.apply_for_team, name='apply'),
    path('application/<int:app_id>/<str:action>/', views.review_application, name='review_application'),
]
