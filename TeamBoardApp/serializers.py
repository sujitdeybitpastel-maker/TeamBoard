from rest_framework import serializers
from .models import EmployeesTest

class EmployeesTestSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='f_name')
    last_name = serializers.CharField(source='l_name')

    class Meta:
        model = EmployeesTest
        fields = ['id', 'first_name', 'last_name', 'email']
