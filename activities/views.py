from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from .models import Activity
from .serializers import UserSerializer, ActivitySerializer, ActivityHistorySerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.
    Provides CRUD operations for User model.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """
        Get all activities for a specific user.
        """
        user = self.get_object()
        activities = Activity.objects.filter(user=user)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing activities.
    Provides CRUD operations for Activity model.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_queryset(self):
        """
        Optionally filter activities by user_id query parameter.
        """
        queryset = Activity.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    @action(detail=False, methods=['get'])
    def history(self, request):
        """
        Get activity history with optional filtering and statistics.
        
        Query parameters:
        - user_id: Filter by user ID
        - days: Number of days to look back (default: 30)
        - activity_type: Filter by activity type
        """
        queryset = self.get_queryset()
        
        # Filter by user_id if provided
        user_id = request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        # Filter by activity_type if provided
        activity_type = request.query_params.get('activity_type', None)
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        # Filter by days if provided
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now().date() - timedelta(days=days)
        queryset = queryset.filter(date__gte=start_date)
        
        # Get statistics
        stats = {
            'total_activities': queryset.count(),
            'total_duration': queryset.aggregate(Sum('duration'))['duration__sum'] or 0,
            'total_distance': queryset.aggregate(Sum('distance'))['distance__sum'] or 0,
            'total_calories': queryset.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0,
            'average_duration': queryset.aggregate(Avg('duration'))['duration__avg'] or 0,
            'activities_by_type': queryset.values('activity_type').annotate(
                count=Count('id')
            ).order_by('-count'),
        }
        
        # Serialize activities
        serializer = ActivityHistorySerializer(queryset, many=True)
        
        return Response({
            'statistics': stats,
            'activities': serializer.data,
            'period': f'Last {days} days'
        })

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get summary statistics for all activities or filtered by user.
        """
        queryset = self.get_queryset()
        
        user_id = request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        summary = {
            'total_activities': queryset.count(),
            'total_duration_minutes': queryset.aggregate(Sum('duration'))['duration__sum'] or 0,
            'total_distance_km': queryset.aggregate(Sum('distance'))['distance__sum'] or 0,
            'total_calories_burned': queryset.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0,
            'activities_by_type': queryset.values('activity_type').annotate(
                count=Count('id'),
                total_duration=Sum('duration'),
                total_distance=Sum('distance')
            ).order_by('-count'),
        }
        
        return Response(summary)


