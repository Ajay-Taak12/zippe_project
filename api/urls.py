from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication
    path('auth/register/', views.UserRegistrationView.as_view(), name='register'),
    path('auth/login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', views.CurrentUserView.as_view(), name='current_user'),
    
    # Tasks
    path('tasks/', views.TaskListCreateView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    
    # Users (admin only)
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
]