from django.urls import path
from .views import PlacementListCreateView, WeeklyLogListCreateView

urlpatterns = [
    path('applications/', PlacementListCreateView.as_view(), name='placement-list'),
    path('logs/', WeeklyLogListCreateView.as_view(), name='weekly-logs'),
]