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
from .views import IndexView, poll_crerate,  DetailView, choice_create, VoteView, PollDeleteView


urlpatterns = [
    path('', IndexView.as_view(), name='polls'),
    path('polls_create/', poll_crerate, name='polls_create'),
    path('<int:pk>/choice_create/', choice_create, name='choice_create'),
    path('<int:pk>/', DetailView.as_view(), name='poll_detail'),
    path('<int:poll_id>/vote/', VoteView.as_view(), name='polls_vote'),
    path('delete/<int:pk>/', PollDeleteView.as_view(), name='poll_delete'),
]
