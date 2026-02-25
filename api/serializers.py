from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, UserProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,style={'input_type':'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'}, label="Confirm password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'email':{'required':True}
        }

    def validate(self,data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self,validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
    
class UserSerializer(serializers.ModelSerializer):
    role =  serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'email','role']
    def get_role(self,obj):
        return obj.profile.role if hasattr(obj, 'profile') else 'user'


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'updated_at', 'user', 'user_id']
        read_only_fields = ['created_at', 'updated_at']

class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']
