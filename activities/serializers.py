from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Activity


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    activities_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'activities_count']
        read_only_fields = ['id', 'date_joined']

    def get_activities_count(self, obj):
        return obj.activities.count()


class ActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for Activity model.
    """
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Activity
        fields = [
            'id', 'user', 'user_id', 'activity_type', 'duration',
            'distance', 'calories_burned', 'notes', 'date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        # If user_id is provided, use it; otherwise use the request user
        user_id = validated_data.pop('user_id', None)
        if user_id:
            validated_data['user_id'] = user_id
        elif self.context.get('request') and self.context['request'].user.is_authenticated:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ActivityHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for activity history with aggregated data.
    """
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Activity
        fields = [
            'id', 'user', 'activity_type', 'duration',
            'distance', 'calories_burned', 'notes', 'date',
            'created_at', 'updated_at'
        ]


