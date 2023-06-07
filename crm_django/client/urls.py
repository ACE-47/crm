
from django.urls import path
from . import views

urlpatterns = [
    path('',views.clients_list,name='clients-list' ),
    path('<int:pk>/', views.client_details,name='client-details'),
    # path('<int:pk>/add-comment', views.client_details,name='add-comment'),
    path('add-client/', views.add_client,name='add-client'),
    path('<int:pk>/delete/', views.delete_client,name='client-delete'),
    path('<int:pk>/edit/', views.edit_client,name='edit-client'),
    path('<int:pk>/add-file/', views.add_file,name='add-file'),

]