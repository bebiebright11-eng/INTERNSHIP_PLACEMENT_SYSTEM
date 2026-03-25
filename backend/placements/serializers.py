from rest_framework import serializers
from .models import InternshipPlacement, WeeklyLog

class InternshipPlacementSerializer(serializers.ModelSerializer):
    # We use these to show the names in the JSON response
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    organization_name = serializers.CharField(source='organizations.name', read_only=True)

    class Meta:
        model = InternshipPlacement
        fields = [
            'id', 'student', 'student_name', 'organizations', 
            'organization_name', 'status', 'workplace_supervisor', 
            'academic_supervisor', 'final_score'
        ]
        read_only_fields = ['status', 'final_score', 'academic_supervisor']

class WeeklyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyLog
        fields = '__all__'
        extra_kwargs = {
            'placement': {'required': False},
            'week_number': {'required': False},
            'tasks_performed': {'required': False},
        }

    def validate(self, data):
        # 1. Try to get placement from the data (for New Logs)
        placement = data.get('placement')
        
        # 2. If placement is NOT in the data (like in a PATCH request), 
        #    we check the existing instance if it's an update.
        if placement is None and self.instance:
            placement = self.instance.placement

        # 3. Now check the status only if we actually have a placement object
        if placement:
            if placement.status != 'approved':
                raise serializers.ValidationError(
                    "You cannot submit weekly logs until your internship placement has been approved."
                )
        
        return data