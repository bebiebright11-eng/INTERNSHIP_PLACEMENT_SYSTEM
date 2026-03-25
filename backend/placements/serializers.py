from rest_framework import serializers
from .models import InternshipPlacement, WeeklyLog

class InternshipPlacementSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    # Match this to your field name (organizations with an 's')
    organization_name = serializers.CharField(source='organizations.name', read_only=True)

    class Meta:
        model = InternshipPlacement
        fields = [
            'id', 'student', 'student_name', 'organizations', 
            'organization_name', 'status', 'workplace_supervisor', 
            'academic_supervisor', 'grade', 'final_report', 'report_submitted_at'
        ]
        # Added report fields and grade to read_only where necessary
        read_only_fields = ['status', 'grade', 'academic_supervisor', 'report_submitted_at']

class WeeklyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyLog
        fields = [
            'id', 'placement', 'week_number', 'tasks_performed', 
            'challenges', 'attendance_days', 'workplace_feedback', 
            'academic_feedback', 'is_verified_by_workplace', 'status', 'submitted_at'
        ]
        # Added the new feedback fields to read_only for the student
        read_only_fields = [
            'week_number', 'workplace_feedback', 'academic_feedback', 
            'is_verified_by_workplace', 'status', 'submitted_at'
        ]

    def validate(self, data):
        placement = data.get('placement')
        
        if placement is None and self.instance:
            placement = self.instance.placement

        if placement:
            # Note: Ensure this matches the string in your Admin Action ('APPROVED')
            if placement.status.upper() != 'APPROVED':
                raise serializers.ValidationError(
                    "You cannot submit weekly logs until your internship placement has been approved."
                )
        
        return data