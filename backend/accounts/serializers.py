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

class AcademicSupervisorRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # This must match your Profile Serializer for the department field
    profile = AcademicSupervisorProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')

        # FORCE the role to 'academic_sup'
        # No matter what the frontend sends, this user will be a Supervisor
        user = User.objects.create(
            role='academic_sup', 
            **validated_data
        )
        
        user.set_password(password)
        user.save()

        # Create the linked AcademicSupervisorProfile
        # We use the 'user' we just created to link it
        AcademicSupervisorProfile.objects.create(
            user=user, 
            **profile_data
        )

        return user       

# --- 3. Registration Serializer (THE ADDITION) ---
class StudentRegistrationSerializer(serializers.ModelSerializer):
    # We add a password field and the nested profile fields
    password = serializers.CharField(write_only=True)
    profile = StudentProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')

        # 1. Create the User
        user = User.objects.create(role='student', **validated_data)
        user.set_password(password)
        user.save()

        # 2. Update the Profile (Force the data in)
        StudentProfile.objects.update_or_create(
            user=user, 
            defaults={
                'registration_number': profile_data.get('registration_number'),
                'course': profile_data.get('course'),
                'year_of_study': profile_data.get('year_of_study'),
            }
        )

        # 3. THE MAGIC LINE: Refresh the user instance
        # This tells Django: "Go back to the DB and get the NEWEST profile data"
        user.refresh_from_db()

        return user
# --- 4. Display Serializers (For React GET requests) ---
class StudentUserSerializer(serializers.ModelSerializer):
    profile = StudentProfileSerializer(source='student_profile', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

class WorkplaceSupervisorUserSerializer(serializers.ModelSerializer):
    profile = WorkplaceSupervisorProfileSerializer(source='workplace_profile')
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']


class WorkplaceSupervisorRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = WorkplaceSupervisorProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')

        # FORCE the role to 'workplace_sup'
        user = User.objects.create(
            role='workplace_sup', 
            **validated_data
        )
        
        user.set_password(password)
        user.save()

        # Link to the organization provided in the profile data
        WorkplaceSupervisorProfile.objects.create(
            user=user, 
            **profile_data
        )

        return user        




