from rest_framework import serializers
from .models import User, StudentProfile, WorkplaceSupervisorProfile, AcademicSupervisorProfile

# --- 1. Base User Serializer (For simple data) ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']

# --- 2. Profile Serializers (The Details) ---
class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['registration_number', 'course', 'year_of_study', 'is_eligible', 'cv']

class WorkplaceSupervisorProfileSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organizations.name', read_only=True)
    class Meta:
        model = WorkplaceSupervisorProfile
        fields = ['organizations', 'organization_name', 'job_title']

class AcademicSupervisorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSupervisorProfile
        fields = ['department']

# --- 3. Registration Serializer (THE ADDITION) ---
class StudentRegistrationSerializer(serializers.ModelSerializer):
    # We add a password field and the nested profile fields
    password = serializers.CharField(write_only=True)
    profile = StudentProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'profile']

    def create(self, validated_data):
        # Extract the nested data
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')

        # Create user instance (role defaults to student in your model)
        user = User.objects.create(**validated_data)
        
        # Security: Hash the password properly
        user.set_password(password)
        user.save()

        # Update the profile that was automatically created by your signals.py
        StudentProfile.objects.update_or_create(user=user, defaults=profile_data)

        return user

# --- 4. Display Serializers (For React GET requests) ---
class StudentUserSerializer(serializers.ModelSerializer):
    profile = StudentProfileSerializer(source='student_profile')
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

class WorkplaceSupervisorUserSerializer(serializers.ModelSerializer):
    profile = WorkplaceSupervisorProfileSerializer(source='workplace_profile')
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']




