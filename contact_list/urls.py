'''
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
'''


from django.urls import path
from .views import ContactListView, ContactCreateView, ContactDetailView, ContactDeleteView, ContactEditView


urlpatterns = [
    path('', ContactListView.as_view(), name='contact_list'),
    path('create_contact/', ContactCreateView.as_view(), name='contact_create'),
    path('<int:pk>/', ContactDetailView.as_view(), name='contact_detail'),
    path('delete/<int:pk>/', ContactDeleteView.as_view(), name='contact_delete'),
    path('edit/<int:pk>/', ContactEditView.as_view(), name='contact_edit'),
]
