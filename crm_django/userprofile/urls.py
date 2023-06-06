from django.contrib.auth import views as vs
from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.signup,name='signup'),
    path('log-in/',vs.LoginView.as_view(template_name = 'userprofile/login.html',),name='login'),
    path('log-out/',vs.LogoutView.as_view(),name='logout'),
    path('my-account',views.account,name='my-account'),

]