
from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.team_detail,name='team-detail'),
    path('<int:pk>/edit/', views.edit_team,name='edit-team'),

]