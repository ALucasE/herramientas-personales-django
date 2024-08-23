from django.urls import path
from .views import (
    EventList,
    EventCreate,
    EventDetail,
    EventUpdate,
    EventDelete,
    full_calendar,
    EventJSONList,
)

urlpatterns = [
    path('calendar/', full_calendar, name='personal_planner_full_calendar'),
    path('eventos/json/', EventJSONList.as_view(), name='personal_planner_full_calendar_api'),
    path('', EventList.as_view(), name='personal_planner'),
    path('create/', EventCreate.as_view(), name='personal_planner_create'),
    path('<slug:slug>/', EventDetail.as_view(), name='personal_planner_detail'),
    path('<slug:slug>/edit/', EventUpdate.as_view(), name='personal_planner_edit'),
    path('<slug:slug>/delete/', EventDelete.as_view(), name='personal_planner_delete'),
]
