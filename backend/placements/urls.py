from django.urls import path
from .views import PlacementListCreateView, WeeklyLogListCreateView,SupervisorLogReviewView

urlpatterns = [
    path('applications/', PlacementListCreateView.as_view(), name='placement-list'),
    path('logs/', WeeklyLogListCreateView.as_view(), name='weekly-logs'),
    path('logs/review/<int:pk>/', SupervisorLogReviewView.as_view(), name='log-review'),
]

