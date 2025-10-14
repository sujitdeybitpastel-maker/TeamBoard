from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Employees
from django.db import models
from .serializers import EmployeesSerializer, EmployeesCreateSerializer
from django.utils import timezone
from django.contrib.auth.hashers import make_password

# Fetch all employees Details
@api_view(['POST'])
def employee_list(request):
    payload = request.data
    emp_id = payload.get('id')
    data_limit = payload.get('limit')
    page_no = payload.get('page', 1)

    data = []

    try:
        if emp_id:
            # Fetch a single employee by ID
            try:
                emp = Employees.objects.get(id=emp_id)
                serializer = EmployeesSerializer(emp)
                data.append(serializer.data)
                message = "Employee retrieved successfully"
            except Employees.DoesNotExist:
                return Response({
                    "status": "Error",
                    "message": "No employee found",
                    "data": []
                }, status=status.HTTP_404_NOT_FOUND)

        elif data_limit and page_no:
            # Fetch paginated employee list
            try:
                data_limit = int(data_limit)
                page_no = int(page_no)
            except ValueError:
                return Response({
                    "status": "Error",
                    "message": "limit and page must be integers",
                    "data": []
                }, status=status.HTTP_400_BAD_REQUEST)

            employees = Employees.objects.all().order_by('id')
            start = (page_no - 1) * data_limit
            end = start + data_limit
            paginated_employees = employees[start:end]
            serializer = EmployeesSerializer(paginated_employees, many=True)
            data = serializer.data
            if len(data) == 0:
                return Response({
                    "status": "Error",
                    "message": "Employee data not found",
                    "data": []
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                message = "Employees retrieved successfully"

        elif not payload:
            # Fetch all employees if payload is empty
            employees = Employees.objects.all().order_by('id')
            serializer = EmployeesSerializer(employees, many=True)
            data = serializer.data
            message = "Employees retrieved successfully"

        else:
            # Invalid input
            return Response({
                "status": "Error",
                "message": "Invalid Input",
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": "OK",
            "message": message,
            "data": data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": "Error",
            "message": f"Internal Server Error: {str(e)}",
            "data": []
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# POST create employee
@csrf_exempt 
def employee_create(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            first_name = body.get("first_name")
            last_name = body.get("last_name")
            email = body.get("email")
            password = body.get("password")
            phone_number = body.get("phone_number")
            address = body.get("address")
            profile_image_url = body.get("profile_image_url")
            system_creation_time = timezone.now()
            system_update_time = timezone.now()
            status = 1
            last_id = Employees.objects.aggregate(max_id=models.Max('id'))['max_id'] or 0
            new_id = last_id + 1
            existing_count_email = Employees.objects.filter(
                        email=email
                            ).exclude(status=5).count()
            existing_count_phone = Employees.objects.filter(
                        phone_number=phone_number
                            ).exclude(status=5).count()

            print('------------------------',first_name,address)

            if not first_name:
                return JsonResponse({
                    "status": "Error",
                    "message": "Enter First Name"
                }, status=409)
            if not email:
                return JsonResponse({
                    "status": "Error",
                    "message": "Please Enter Email Address"
                }, status=409)
            if existing_count_email>=1:
                return JsonResponse({
                    "status": "Error",
                    "message": "Duplicate Email Address Please Enter Unique one"
                }, status=409)
            if not phone_number:
                return JsonResponse({
                    "status": "Error",
                    "message": "Please Enter Phone Number"
                }, status=409)
            if existing_count_phone>=1:
                return JsonResponse({
                    "status": "Error",
                    "message": "Duplicate Phone Number Please Enter Unique one"
                }, status=409)
            if not address:
                return JsonResponse({
                    "status": "Error",
                    "message": "Please Enter Address"
                }, status=409)
            
        # 1. First_name mandatory not unique
        # 2. email mandatory and unique
        # 3. password mandatory and hashed
        # 4. phone_number mandatory and unique
        # 5. system_creation_time mandatory
        # 6. Address mandatory
            # create employee using ORM
            hashed_password = make_password(password)
            employee = Employees.objects.create(
                id = new_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password = hashed_password,
                phone_number = phone_number,
                address = address,
                profile_image_url = profile_image_url,
                system_creation_time = system_creation_time,
                system_update_time = system_update_time,
                status = status
            )
            serializer = EmployeesCreateSerializer(employee)
            return JsonResponse({
                "status": "OK",
                "message": "Employee created successfully",
                "data": serializer.data
                
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({
                "status": "Error",
                "message": "Invalid JSON"
            }, status=400)