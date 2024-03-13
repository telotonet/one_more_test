from django.urls import path
from .views import EventCreateView, OrganizationCreateView, EventDetailView, EventFilterListView

urlpatterns = [
    path('create/event/', EventCreateView.as_view(), name='event-create'),
    path('create/organization/', OrganizationCreateView.as_view(), name='organization-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/', EventFilterListView.as_view(), name='event-list'),
]