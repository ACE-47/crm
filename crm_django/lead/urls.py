from django.urls import path
from . import views

urlpatterns = [
    path('', views.LeadListView.as_view(),name='leads-list'),
    path('<int:pk>/', views.LeadDetailView.as_view(),name='lead-details'),
    path('<int:pk>/delete/', views.LeadDeleteView.as_view(),name='lead-delete'),
    path('<int:pk>/edit/', views.LeadUpdateView.as_view(),name='edit-lead'),
    path('<int:pk>/convert/', views.ConvertToClientView.as_view(),name='lead-convert'),
    path('add-lead/', views.LeadCreateView.as_view(),name='add-lead'),
    path('<int:pk>/add-comment/', views.AddCommentView.as_view(),name='add-comment'),
    path('<int:pk>/add-file/', views.AddFileView.as_view(),name='add-file'),

]