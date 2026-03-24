from django.urls import path
from .views import OrganizationListCreateView, OrganizationRetrieveUpdateDestroyView

urlpatterns = [
    path('', OrganizationListCreateView.as_view(), name='organization-list'),
    path('<int:pk>/', OrganizationRetrieveUpdateDestroyView.as_view(), name='organization-detail'),
]