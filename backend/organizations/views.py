from rest_framework import generics, permissions
from .models import Organization
from .serializers import OrganizationSerializer

# List all organizations (GET) or Create a new one (POST)
class OrganizationListCreateView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            # Only allow logged-in users to create organizations
            return [permissions.IsAuthenticated()]
        # Allow anyone (even unauthenticated students) to view the list
        return [permissions.AllowAny()]

# Retrieve, Update, or Delete a single organization
class OrganizationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]