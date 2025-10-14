from rest_framework import serializers
from .models import EmployeesTest
from .models import Employees

class EmployeesTestSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='f_name')
    last_name = serializers.CharField(source='l_name')
    #email = serializers.CharField(source='email')

    class Meta:
        model = EmployeesTest
        fields = ['id', 'first_name', 'last_name', 'email']


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
