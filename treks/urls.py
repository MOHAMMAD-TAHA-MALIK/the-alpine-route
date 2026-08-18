from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Navigation & List Views
    path('', views.trek_list, name='trek_list'),
    path('upcoming/', views.upcoming_treks, name='upcoming_treks'),
    path('previous/', views.previous_treks, name='previous_treks'),

    # Authentication & User Management
    path('register/', views.register, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-change/', views.change_password, name='change_password'),

    # Trek Creation & Participation
    path('trek/new/', views.create_trek, name='create_trek'),
    path('trek/<int:pk>/join/', views.join_trek, name='join_trek'),

    # Trek Event Details & Interaction
    path('trek/<int:pk>/', views.trek_detail, name='trek_detail'),
    path('trek/<int:pk>/like/', views.like_event, name='like_event'),
    path('trek/<int:pk>/comment/', views.add_comment, name='add_comment'),


    path('event/new/', views.create_trek_event, name='create_trek_event'),
    path('trek/<int:pk>/leave/', views.leave_trek, name='leave_trek'),
    path('profile/', views.profile, name='profile'),
]