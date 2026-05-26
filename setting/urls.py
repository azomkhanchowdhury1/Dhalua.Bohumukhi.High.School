"""
URL configuration for satting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', accounts_views.home_view, name='home'),
    path('about/', accounts_views.about_view, name='about'),
    path('academics/', accounts_views.academics_view, name='academics'),
    path('admission/', accounts_views.admission_view, name='admission'),
    path('contact/', accounts_views.contact_view, name='contact'),
    path('gallery/', accounts_views.gallery_view, name='gallery'),
    path('support/', accounts_views.support_view, name='support'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('admin-dashboard/', include('admin.urls')),
    path('students/', include('student.urls')),
    path('teachers/', include('teacher.urls')),
    path('staff/', include('staff.urls')),
    path('parents/', include('prents.urls')),
    path('notices/', include('notices.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
