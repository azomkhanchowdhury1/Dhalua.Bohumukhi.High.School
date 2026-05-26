from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('otp-verify/', views.otp_verify_view, name='otp_verify'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('global-search/', views.global_search, name='global_search'),
]
