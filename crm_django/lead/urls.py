from django.urls import path
from . import views

urlpatterns = [
    path('', views.LeadListView.as_view(),name='leads-list'),
    path('<int:pk>/', views.lead_details,name='lead-details'),
    path('<int:pk>/delete/', views.lead_delete,name='lead-delete'),
    path('<int:pk>/edit/', views.edit_lead,name='edit-lead'),
    path('<int:pk>/convert/', views.convert_to_client,name='lead-convert'),
    path('add-lead/', views.add_lead,name='add-lead'),
]