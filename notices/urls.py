from django.urls import path
from . import views

# START: NOTICE_URLS
app_name = 'notices'

urlpatterns = [
    path('', views.notice_list, name='notice_list'),
]
# END: NOTICE_URLS
