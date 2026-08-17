from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.trek_list, name='trek_list'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-change/', views.change_password, name='change_password'),
    path('trek/new/', views.create_trek, name='create_trek'),
    path('trek/<int:pk>/join/', views.join_trek, name='join_trek'),
]