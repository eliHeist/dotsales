from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # password change
    path('password_change/', views.LogoutView.as_view(), name='password_change'),
    path('password_change_done/', views.LogoutView.as_view(), name='password_change_done'),
    # password reset
    path('reset_password/', views.PasswordResetView.as_view(), name='reset_password'),
    path('password_reset_done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]