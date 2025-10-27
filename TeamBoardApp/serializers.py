from rest_framework import serializers
from .models import Employees,Project,ProjectMembership,Message
import hashlib

def generate_hashed_id(value):
    """Utility to hash any integer/string ID."""
    return hashlib.md5(str(value).encode()).hexdigest() if value else None

class EmployeesCreateSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()  # override the default 'id' field

    class Meta:
        model = Employees
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address',
            'profile_image_url',
            'system_creation_time',
            'system_update_time',
            'status'
        ]

    def get_id(self, obj):
        """Return the hashed version of the employee's ID."""
        return hashlib.md5(str(obj.id).encode()).hexdigest()
        # 1. First_name mandatory not unique
        # 2. email mandatory and unique
        # 3. password mandatory and hashed
        # 4. phone_number mandatory and unique
        # 5. system_creation_time mandatory

class EmployeesSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    class Meta:
        model = Employees
        fields = ['id', 'first_name', 'last_name', 'email','phone_number','address','profile_image_url','status']

    def get_id(self, obj):
        """Return the hashed version of the employee's ID."""
        return hashlib.md5(str(obj.id).encode()).hexdigest()

class ProjectCreateSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['id', 'title','description','banner_image_url','system_creation_time','status']

    def get_id(self, obj):
        """Return the hashed version of the employee's ID."""
        return hashlib.md5(str(obj.id).encode()).hexdigest()

class ProjectsSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['id', 'title','description','banner_image_url','status']
    def get_id(self, obj):
        """Return the hashed version of the employee's ID."""
        return hashlib.md5(str(obj.id).encode()).hexdigest()

# Need to check here the hasing
class MemberSerializer(serializers.ModelSerializer):
    """
    This class fetch the data from employee table. In project_memberships table the fk are member_id ==id of employee and project_id == id of project table..
    """
    id = serializers.IntegerField(source='employees.id', read_only=True)
    id = serializers.SerializerMethodField()
    first_name = serializers.CharField(source='employees.first_name', read_only=True)
    email = serializers.EmailField(source='employees.email', read_only=True)
    phone_number = serializers.EmailField(source='employees.phone_number', read_only=True)

    class Meta:
        model = ProjectMembership
        fields = ['id', 'first_name', 'email','phone_number', 'is_admin', 'status']
    
    def get_id(self, obj):
        """Return the hashed version of the employee's ID."""
        return hashlib.md5(str(obj.id).encode()).hexdigest()


class ProjectSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'banner_image_url', 'status', 'members']

    def get_members(self, obj):
        # Filter memberships where status != '5'
        active_memberships = obj.memberships.exclude(status='5')
        return MemberSerializer(active_memberships, many=True).data
    def get_id(self, obj):
        """Return the hashed version of the employee's ID."""
        return hashlib.md5(str(obj.id).encode()).hexdigest()

class AddMemberSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    project_id = serializers.SerializerMethodField()
    member_id = serializers.SerializerMethodField()
    class Meta:
        model = ProjectMembership
        fields = ['id', 'project_id', 'member_id', 'is_admin'] # Chnage the name of employees_id -->> member_id
    def get_id(self, obj):
        """Hash the membership record ID."""
        return generate_hashed_id(obj.id)

    def get_project_id(self, obj):
        """Hash the related project ID."""
        return generate_hashed_id(obj.project_id)

    def get_member_id(self, obj):
        """Return the hashed employee ID, key shown as member_id."""
        return generate_hashed_id(obj.employees_id)

# change the name of employee_id to Member_id
class RemoveMemberSerializer(serializers.ModelSerializer):
    member_id = serializers.SerializerMethodField()
    project_id = serializers.SerializerMethodField()

    class Meta:
        model = ProjectMembership
        fields = ['project_id', 'member_id'] 

    def get_project_id(self, obj):
        """Hash the related project ID."""
        return generate_hashed_id(obj.project_id)

    def get_member_id(self, obj):
        """Return the hashed employee ID, key shown as member_id."""
        return generate_hashed_id(obj.employees_id)

# class ProjectMemberSerializer(serializers.ModelSerializer):
#     members = MemberSerializer(source='memberships', many=True, read_only=True)

#     class Meta:
#         model = Employees
#         fields = []

class ProjectMemberSerializer(serializers.ModelSerializer):
    # Pull fields from the related Employees model
    id = serializers.IntegerField(source='employees.id', read_only=True)
    id = serializers.SerializerMethodField()
    first_name = serializers.CharField(source='employees.first_name', read_only=True)
    
    # Field from ProjectMembership itself
    is_admin = serializers.BooleanField(read_only=True)

    class Meta:
        model = ProjectMembership
        fields = ['id', 'first_name', 'is_admin']

    def get_id(self, obj):
        """Return the hashed version of the employee's ID."""
        return hashlib.md5(str(obj.id).encode()).hexdigest()


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    project_id = serializers.SerializerMethodField()
    member_id = serializers.SerializerMethodField()  # hash employee ID

    class Meta:
        model = Message
        fields = ['id', 'project_id', 'member_id', 'text_body', 'has_media', 'media_url', 'system_creation_time']

    def get_id(self, obj):
        """Return the hashed message ID."""
        return generate_hashed_id(obj.id)

    def get_project_id(self, obj):
        """Return the hashed project ID."""
        return generate_hashed_id(obj.project_id)

    def get_member_id(self, obj):
        """Return the hashed employee ID, key shown as member_id."""
        return generate_hashed_id(obj.employees_id)
    
class ProjectMessagesSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id','sender','text_body','has_media','media_url','system_creation_time']

    def get_id(self, obj):
        """Return the hashed message ID."""
        return hashlib.md5(str(obj.id).encode()).hexdigest()

    def get_sender(self, obj):
        """Return a nested sender object with hashed member_id and first_name."""
        return {
            "id": generate_hashed_id(obj.employees_id),
            "first_name": obj.employees.first_name if obj.employees else None
        }


class EmployeeMessagesSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id','project','text_body','has_media','media_url','system_creation_time']

    def get_id(self, obj):
        """Return the hashed message ID."""
        return hashlib.md5(str(obj.id).encode()).hexdigest()

    def get_project(self, obj):
        """Return a nested projects object with hashed project_id and first_name."""
        return {
            "id": generate_hashed_id(obj.project_id),
            "title": obj.project.title if obj.project else None
        }