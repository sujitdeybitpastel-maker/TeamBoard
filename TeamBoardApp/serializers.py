from rest_framework import serializers
from .models import Employees,Project,ProjectMembership,Message

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

class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title','description','banner_image_url','status']


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
    members = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'banner_image_url', 'status', 'members']

    def get_members(self, obj):
        # Filter memberships where status != '5'
        active_memberships = obj.memberships.exclude(status='5')
        return MemberSerializer(active_memberships, many=True).data



class AddMemberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProjectMembership
        fields = ['id', 'project_id', 'employees_id', 'is_admin'] # Chnage the name of employees_id -->> member_id

class RemoveMemberSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField(source='employees.id', read_only=True)
    class Meta:
        model = ProjectMembership
        fields = ['project_id', 'member_id']

# class ProjectMemberSerializer(serializers.ModelSerializer):
#     members = MemberSerializer(source='memberships', many=True, read_only=True)

#     class Meta:
#         model = Employees
#         fields = []

class ProjectMemberSerializer(serializers.ModelSerializer):
    # Pull fields from the related Employees model
    id = serializers.IntegerField(source='employees.id', read_only=True)
    first_name = serializers.CharField(source='employees.first_name', read_only=True)
    
    # Field from ProjectMembership itself
    is_admin = serializers.BooleanField(read_only=True)

    class Meta:
        model = ProjectMembership
        fields = ['id', 'first_name', 'is_admin']


class MessageSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField(source='employees.id', read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'project_id','member_id','text_body','has_media', 'media_url','system_creation_time']

