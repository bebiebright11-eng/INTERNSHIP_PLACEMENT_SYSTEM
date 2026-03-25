from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import (
    StudentRegistrationSerializer, 
    StudentUserSerializer, 
    WorkplaceSupervisorUserSerializer,
    AcademicSupervisorRegistrationSerializer
)
from .models import User

# 1. Student Registration View (POST)
class StudentRegistrationView(generics.CreateAPIView):
    serializer_class = StudentRegistrationSerializer
    permission_classes = [permissions.AllowAny] # Anyone can register

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Automatically create a token so they are logged in after registering
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": StudentUserSerializer(user).data,
                "token": token.key,
                "message": "Registration successful!"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 2. Custom Login View (POST)
class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # Determine which serializer to use based on the user's role
        if user.role == 'student':
            user_data = StudentUserSerializer(user).data
        elif user.role == 'workplace_sup':
            user_data = WorkplaceSupervisorUserSerializer(user).data
        else:
            # Fallback for admin or academic supervisor
            user_data = {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }

        return Response({
            "token": token.key,
            "user": user_data
        })

# 3. User Profile View (GET - retrieves data for the logged-in user)
class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == 'student':
            serializer = StudentUserSerializer(user)
        elif user.role == 'workplace_sup':
            serializer = WorkplaceSupervisorUserSerializer(user)
        else:
            return Response({"username": user.username, "role": user.role})
            
        return Response(serializer.data)
    




class AcademicSupervisorRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class =AcademicSupervisorRegistrationSerializer