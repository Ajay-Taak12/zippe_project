from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
# from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import (
    UserRegistrationSerializer, 
    UserSerializer, 
    TaskSerializer, 
    TaskCreateUpdateSerializer
)
from .permissions import IsOwnerOrAdmin, IsAdminUser


class UserRegistrationView(generics.CreateAPIView):
    """
    Register a new user
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserSerializer(user).data,
                "message": "User created successfully",
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain view that returns user data along with tokens
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data['username'])
            response.data['user'] = UserSerializer(user).data
        return response

class TaskListCreateView(generics.ListCreateAPIView):
    """
    List all tasks or create a new task
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['completed']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'title', 'completed']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateUpdateSerializer
        return TaskSerializer
    
    def get_queryset(self):
        # Admin can see all tasks, regular users see only their own
        if hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'admin':
            return Task.objects.all()
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a task instance
    """
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TaskCreateUpdateSerializer
        return TaskSerializer
    
    def get_queryset(self):
        # Admin can access any task, regular users only their own
        if hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'admin':
            return Task.objects.all()
        return Task.objects.filter(user=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save()

class UserListView(generics.ListAPIView):
    """
    List all users (admin only)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

class UserDetailView(generics.RetrieveAPIView):
    """
    Retrieve user details (admin only)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class CurrentUserView(generics.RetrieveAPIView):
    """
    Get current user details
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user