from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .serializers import (
    StudentRegistrationSerializer, 
    StudentUserSerializer, 
    WorkplaceSupervisorUserSerializer,
    AcademicSupervisorRegistrationSerializer,
    WorkplaceSupervisorRegistrationSerializer,
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
class UserProfileView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    # Use the serializer that knows about the 'profile' source
    serializer_class = StudentUserSerializer 

    def get_object(self):
        # This tells the view to always grab the logged-in user
        return self.request.user

    def patch(self, request, *args, **kwargs):
        # 1. Get the user and their profile
        user = self.get_object()
        profile = user.student_profile
        
        # 2. Look inside the 'profile' box in your Postman message
        profile_data = request.data.get('profile', {})
        
        # 3. If 'is_eligible' is in there, save it!
        if 'is_eligible' in profile_data:
            profile.is_eligible = profile_data['is_eligible']
            profile.save()
            
        # 4. Send back the updated data
        serializer = self.get_serializer(user)
        return Response({
            "message": "Eligibility updated successfully",
            "is_eligible": profile.is_eligible,
            "profile": serializer.data['profile']
        })
class AcademicSupervisorRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class =AcademicSupervisorRegistrationSerializer


class WorkplaceSupervisorRegistrationView(generics.CreateAPIView):
    serializer_class = WorkplaceSupervisorRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": WorkplaceSupervisorUserSerializer(user).data,
                "token": token.key,
                "message": "Workplace Supervisor registered successfully!"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    