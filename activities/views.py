from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta, datetime
from .models import Activity
from .serializers import UserSerializer, ActivitySerializer, ActivityHistorySerializer
from .permissions import IsOwnerOrReadOnly, IsOwner, IsUserOwner


class RegisterView(APIView):
    """
    View for user registration.
    Public endpoint - no authentication required.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User created successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.
    Provides CRUD operations for User model.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]  # Allow anyone to register
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsUserOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, IsUserOwner])
    def activities(self, request, pk=None):
        """
        Get all activities for a specific user.
        Only the user themselves can access their activities.
        """
        user = self.get_object()
        if user != request.user:
            return Response(
                {'error': 'You can only view your own activities'},
                status=status.HTTP_403_FORBIDDEN
            )
        activities = Activity.objects.filter(user=user)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing activities.
    Provides CRUD operations for Activity model.
    Users can only manage their own activities.
    """
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Filter activities to only show the authenticated user's activities.
        Optionally filter by user_id query parameter (but only if it's the current user).
        """
        user = self.request.user
        queryset = Activity.objects.filter(user=user)
        
        # Optional filtering by activity_type
        activity_type = self.request.query_params.get('activity_type', None)
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        # Sorting
        sort_by = self.request.query_params.get('sort_by', '-date')
        valid_sort_fields = ['date', '-date', 'duration', '-duration', 'calories_burned', '-calories_burned', 'created_at', '-created_at']
        if sort_by in valid_sort_fields:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('-date', '-created_at')
        
        return queryset

    def perform_create(self, serializer):
        """Ensure the user is set to the current authenticated user."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def history(self, request):
        """
        Get activity history with optional filtering and statistics.
        
        Query parameters:
        - user_id: Filter by user ID (ignored, only shows current user's activities)
        - start_date: Start date (YYYY-MM-DD format)
        - end_date: End date (YYYY-MM-DD format)
        - days: Number of days to look back (default: 30, ignored if start_date/end_date provided)
        - activity_type: Filter by activity type
        - sort_by: Sort by field (date, -date, duration, -duration, calories_burned, -calories_burned)
        """
        queryset = Activity.objects.filter(user=request.user)
        
        # Date range filtering
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        days = request.query_params.get('days', None)
        
        if start_date and end_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                if start_date_obj > end_date_obj:
                    return Response(
                        {'error': 'start_date must be before or equal to end_date'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                queryset = queryset.filter(date__gte=start_date_obj, date__lte=end_date_obj)
                period = f"{start_date} to {end_date}"
            except ValueError:
                return Response(
                    {'error': 'Invalid date format. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__gte=start_date_obj)
                period = f"From {start_date}"
            except ValueError:
                return Response(
                    {'error': 'Invalid date format. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__lte=end_date_obj)
                period = f"Until {end_date}"
            except ValueError:
                return Response(
                    {'error': 'Invalid date format. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif days:
            try:
                days_int = int(days)
                if days_int <= 0:
                    return Response(
                        {'error': 'days must be a positive integer'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                start_date_obj = timezone.now().date() - timedelta(days=days_int)
                queryset = queryset.filter(date__gte=start_date_obj)
                period = f'Last {days_int} days'
            except ValueError:
                return Response(
                    {'error': 'days must be a valid integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # Default to last 30 days
            start_date_obj = timezone.now().date() - timedelta(days=30)
            queryset = queryset.filter(date__gte=start_date_obj)
            period = 'Last 30 days'
        
        # Filter by activity_type if provided
        activity_type = request.query_params.get('activity_type', None)
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        # Sorting
        sort_by = request.query_params.get('sort_by', '-date')
        valid_sort_fields = ['date', '-date', 'duration', '-duration', 'calories_burned', '-calories_burned']
        if sort_by in valid_sort_fields:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('-date', '-created_at')
        
        # Get statistics
        stats = {
            'total_activities': queryset.count(),
            'total_duration': queryset.aggregate(Sum('duration'))['duration__sum'] or 0,
            'total_distance': queryset.aggregate(Sum('distance'))['distance__sum'] or 0,
            'total_calories': queryset.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0,
            'average_duration': round(queryset.aggregate(Avg('duration'))['duration__avg'] or 0, 2),
            'average_distance': round(queryset.aggregate(Avg('distance'))['distance__avg'] or 0, 2),
            'average_calories': round(queryset.aggregate(Avg('calories_burned'))['calories_burned__avg'] or 0, 2),
            'activities_by_type': queryset.values('activity_type').annotate(
                count=Count('id'),
                total_duration=Sum('duration'),
                total_distance=Sum('distance'),
                total_calories=Sum('calories_burned')
            ).order_by('-count'),
        }
        
        # Serialize activities
        serializer = ActivityHistorySerializer(queryset, many=True)
        
        return Response({
            'statistics': stats,
            'activities': serializer.data,
            'period': period
        })

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get summary statistics for the authenticated user's activities.
        """
        queryset = Activity.objects.filter(user=request.user)
        
        # Optional filtering by date range
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        
        if start_date and end_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__gte=start_date_obj, date__lte=end_date_obj)
            except ValueError:
                return Response(
                    {'error': 'Invalid date format. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        summary = {
            'total_activities': queryset.count(),
            'total_duration_minutes': queryset.aggregate(Sum('duration'))['duration__sum'] or 0,
            'total_distance_km': round(queryset.aggregate(Sum('distance'))['distance__sum'] or 0, 2),
            'total_calories_burned': queryset.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0,
            'average_duration_minutes': round(queryset.aggregate(Avg('duration'))['duration__avg'] or 0, 2),
            'average_distance_km': round(queryset.aggregate(Avg('distance'))['distance__avg'] or 0, 2),
            'average_calories_burned': round(queryset.aggregate(Avg('calories_burned'))['calories_burned__avg'] or 0, 2),
            'activities_by_type': queryset.values('activity_type').annotate(
                count=Count('id'),
                total_duration=Sum('duration'),
                total_distance=Sum('distance'),
                total_calories=Sum('calories_burned')
            ).order_by('-count'),
        }
        
        return Response(summary)

    @action(detail=False, methods=['get'])
    def trends(self, request):
        """
        Get activity trends over time (weekly or monthly).
        
        Query parameters:
        - period: 'weekly' or 'monthly' (default: 'weekly')
        - weeks: Number of weeks to look back (default: 4, only for weekly)
        - months: Number of months to look back (default: 6, only for monthly)
        """
        queryset = Activity.objects.filter(user=request.user)
        
        period = request.query_params.get('period', 'weekly').lower()
        
        if period == 'weekly':
            weeks = int(request.query_params.get('weeks', 4))
            if weeks <= 0:
                return Response(
                    {'error': 'weeks must be a positive integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get start date
            start_date = timezone.now().date() - timedelta(weeks=weeks)
            queryset = queryset.filter(date__gte=start_date)
            
            # Group by week
            trends = []
            for i in range(weeks):
                week_start = start_date + timedelta(weeks=i)
                week_end = week_start + timedelta(days=6)
                week_activities = queryset.filter(date__gte=week_start, date__lte=week_end)
                
                trends.append({
                    'week': f"Week {i+1}",
                    'period': f"{week_start} to {week_end}",
                    'total_activities': week_activities.count(),
                    'total_duration': week_activities.aggregate(Sum('duration'))['duration__sum'] or 0,
                    'total_distance': round(week_activities.aggregate(Sum('distance'))['distance__sum'] or 0, 2),
                    'total_calories': week_activities.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0,
                })
        
        elif period == 'monthly':
            months = int(request.query_params.get('months', 6))
            if months <= 0:
                return Response(
                    {'error': 'months must be a positive integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get start date (approximate, using 30 days per month)
            start_date = timezone.now().date() - timedelta(days=months * 30)
            queryset = queryset.filter(date__gte=start_date)
            
            # Group by month
            trends = []
            current_date = start_date
            for i in range(months):
                # Calculate month start and end
                if current_date.month == 12:
                    month_end = current_date.replace(year=current_date.year + 1, month=1, day=1) - timedelta(days=1)
                else:
                    month_end = current_date.replace(month=current_date.month + 1, day=1) - timedelta(days=1)
                
                month_start = current_date.replace(day=1)
                month_activities = queryset.filter(date__gte=month_start, date__lte=month_end)
                
                trends.append({
                    'month': month_start.strftime('%B %Y'),
                    'period': f"{month_start} to {month_end}",
                    'total_activities': month_activities.count(),
                    'total_duration': month_activities.aggregate(Sum('duration'))['duration__sum'] or 0,
                    'total_distance': round(month_activities.aggregate(Sum('distance'))['distance__sum'] or 0, 2),
                    'total_calories': month_activities.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0,
                })
                
                # Move to next month
                if month_end.month == 12:
                    current_date = month_end.replace(year=month_end.year + 1, month=1, day=1)
                else:
                    current_date = month_end.replace(month=month_end.month + 1, day=1)
        else:
            return Response(
                {'error': "period must be 'weekly' or 'monthly'"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'period_type': period,
            'trends': trends
        })
