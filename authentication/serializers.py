from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    role          = serializers.SerializerMethodField()
    department_id = serializers.SerializerMethodField()
    department    = serializers.SerializerMethodField()
    stream        = serializers.SerializerMethodField()

    class Meta:
        model  = User
        fields = ('id', 'username', 'email', 'role', 'department_id', 'department', 'stream')

    def get_role(self, obj):
        try:
            return obj.profile.role
        except UserProfile.DoesNotExist:
            return 'hod'

    def get_department_id(self, obj):
        try:
            dept = obj.profile.department
            return dept.id if dept else None
        except UserProfile.DoesNotExist:
            return None

    def get_department(self, obj):
        try:
            dept = obj.profile.department
            return dept.name if dept else None
        except UserProfile.DoesNotExist:
            return None

    def get_stream(self, obj):
        try:
            dept = obj.profile.department
            return dept.stream if dept else None
        except UserProfile.DoesNotExist:
            return None