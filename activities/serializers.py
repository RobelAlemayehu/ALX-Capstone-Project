from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Activity


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    activities_count = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'activities_count', 'password']
        read_only_fields = ['id', 'date_joined']

    def get_activities_count(self, obj):
        return obj.activities.count()

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class ActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for Activity model with validation.
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

    def validate_activity_type(self, value):
        """Validate activity type is in allowed choices."""
        valid_types = [choice[0] for choice in Activity.ACTIVITY_TYPES]
        if value not in valid_types:
            raise serializers.ValidationError(
                f"Activity type must be one of: {', '.join(valid_types)}"
            )
        return value

    def validate_duration(self, value):
        """Validate duration is positive."""
        if value <= 0:
            raise serializers.ValidationError("Duration must be greater than 0")
        if value > 1440:  # More than 24 hours
            raise serializers.ValidationError("Duration cannot exceed 1440 minutes (24 hours)")
        return value

    def validate_distance(self, value):
        """Validate distance is positive if provided."""
        if value is not None and value < 0:
            raise serializers.ValidationError("Distance cannot be negative")
        return value

    def validate_calories_burned(self, value):
        """Validate calories burned is positive if provided."""
        if value is not None and value < 0:
            raise serializers.ValidationError("Calories burned cannot be negative")
        return value

    def validate_date(self, value):
        """Validate date is not in the future."""
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError("Date cannot be in the future")
        return value

    def validate(self, data):
        """Cross-field validation."""
        # Ensure required fields are present
        if 'activity_type' not in data:
            raise serializers.ValidationError({"activity_type": "This field is required."})
        if 'duration' not in data:
            raise serializers.ValidationError({"duration": "This field is required."})
        if 'date' not in data:
            raise serializers.ValidationError({"date": "This field is required."})
        return data

    def create(self, validated_data):
        # Always use the authenticated user
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        else:
            raise serializers.ValidationError("User must be authenticated to create activities")
        validated_data.pop('user_id', None)  # Remove user_id if present
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


