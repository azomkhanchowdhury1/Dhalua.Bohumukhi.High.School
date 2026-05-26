from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('dashboard/', views.dashboard, name='staff_dashboard'),
]
