from rest_framework import serializers
from .models import Model1, Model2, Contact
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class Model1Serializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Model1
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']


class Model2Serializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Model2
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['created_at', 'is_read']
