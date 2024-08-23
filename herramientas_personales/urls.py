"""
URL configuration for herramientas_personales project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls import handler404
from django.shortcuts import render

urlpatterns = [
    path('', include('core.urls')),
    path('accounts/', include('registration.urls')),
    path('contact/', include('contact.urls')),
    path('contact_list/', include('contact_list.urls')),
    path('cookbook/', include('cookbook.urls')),
    path('personal_planner/', include('personal_planner.urls')),
    path('polls/', include('polls.urls')),
    path('tasks/', include('tasks.urls')),
    path("admin/", admin.site.urls, name='admin'),
]

# Vista personalizada para el error 404
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

# Asigna la vista personalizada al manejador 404
handler404 = custom_404_view