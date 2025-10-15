from rest_framework import serializers
from .models import Employees,Project,ProjectMembership

class EmployeesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ['id', 'first_name', 'last_name', 'email','phone_number','address','profile_image_url','system_creation_time','system_update_time','status']
        # 1. First_name mandatory not unique
        # 2. email mandatory and unique
        # 3. password mandatory and hashed
        # 4. phone_number mandatory and unique
        # 5. system_creation_time mandatory

class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ['id', 'first_name', 'last_name', 'email','phone_number','address','profile_image_url','status']

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title','description','banner_image_url','system_creation_time','status']


class MemberSerializer(serializers.ModelSerializer):
    """
    This class fetch the data from employee table. In project_memberships table the fk are member_id ==id of employee and project_id == id of project table..
    """
    id = serializers.IntegerField(source='employees.id', read_only=True)
    first_name = serializers.CharField(source='employees.first_name', read_only=True)
    email = serializers.EmailField(source='employees.email', read_only=True)
    phone_number = serializers.EmailField(source='employees.phone_number', read_only=True)

    class Meta:
        model = ProjectMembership
        fields = ['id', 'first_name', 'email','phone_number', 'is_admin', 'status']


class ProjectSerializer(serializers.ModelSerializer):
    members = MemberSerializer(source='memberships', many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'banner_image_url', 'status', 'members']


