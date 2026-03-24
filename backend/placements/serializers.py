from rest_framework import serializers
from .models import InternshipPlacement, WeeklyLog

class WeeklyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyLog
        fields = '__all__'

class InternshipPlacementSerializer(serializers.ModelSerializer):
    # Fetching names from related apps for the React frontend
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    organization_name = serializers.CharField(source='organizations.name', read_only=True)
    academic_supervisor_name = serializers.CharField(source='academic_supervisor.get_full_name', read_only=True)

    class Meta:
        model = InternshipPlacement
        fields = [
            'id', 'student', 'student_name', 'organizations', 'organization_name', 
            'status', 'workplace_supervisor', 'academic_supervisor', 
            'academic_supervisor_name', 'final_score', 'final_evaluation_comments'
        ]
        read_only_fields = ['status', 'student','final_score', 'academic_supervisor']