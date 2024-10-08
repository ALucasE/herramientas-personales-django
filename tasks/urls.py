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


from django.urls import path
from .views import task_create, task_edit, task_detail, tasks_get_all, task_delete

urlpatterns = [
    path('', tasks_get_all , name='tasks'),
    path('task_create/', task_create , name='task_create'),
    path('task_detail/<int:task_id>', task_detail , name='task_detail'),
    path('task_edit/<int:task_id>', task_edit , name='task_edit'),
    path('task_delete/<int:task_id>', task_delete , name='task_delete'),
]
