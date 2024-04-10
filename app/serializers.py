from rest_framework import serializers
from .models import *

'''class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoUsers
        fields = ['name', 'pwd']'''
        
# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        # Create the corresponding TodoUsers instance
        todo_user = TodoUsers.objects.create(username=user)
        return user

    class Meta:
        model = User
        fields = ['username', 'password']    
        
        
class TodoSerializer(serializers.ModelSerializer):
       class Meta:
        model = TodoUsers
        fields ="__all__"   
      