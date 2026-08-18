from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Navigation & List Views
    path('', views.trek_list, name='trek_list'),
    path('upcoming/', views.upcoming_treks, name='upcoming_treks'),
    path('previous/', views.previous_treks, name='previous_treks'),

    # Authentication & User Management
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('password-change/', views.change_password, name='change_password'),

    # Password Reset Flow
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm',
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete',
    ),

    # Staff-Only Creation Views
    path('trek/new/', views.create_trek, name='create_trek'),
    path('event/new/', views.create_trek_event, name='create_trek_event'),

    # Participation Routes
    path('trek/<int:pk>/join/', views.join_trek, name='join_trek'),
    path('trek/<int:pk>/leave/', views.leave_trek, name='leave_trek'),

    # Event Details & Community Interactions
    path('trek/<int:pk>/', views.trek_detail, name='trek_detail'),
    path('trek/<int:pk>/like/', views.like_event, name='like_event'),
    path('trek/<int:pk>/comment/', views.add_comment, name='add_comment'),
]