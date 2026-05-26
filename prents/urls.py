from django.urls import path
from . import views

app_name = 'prents'

urlpatterns = [
    path('dashboard/', views.dashboard, name='parent_dashboard'),
]
