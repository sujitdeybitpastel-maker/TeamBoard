from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
import json
from .models import Employees, Project
from django.db import models
from .serializers import EmployeesSerializer, EmployeesCreateSerializer,ProjectCreateSerializer,ProjectSerializer
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from .authentication import StaticTokenAuthentication

@api_view(['POST'])
@authentication_classes([StaticTokenAuthentication])
@permission_classes([AllowAny])
def employee_list(request):
    payload = request.data
    emp_id = payload.get('id')
    data_limit = payload.get('limit')
    page_no = payload.get('page')

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
    

@api_view(['POST'])
@authentication_classes([StaticTokenAuthentication])
@permission_classes([AllowAny])
def employee_create(request):
    try:
        body = request.data  # DRF automatically parses JSON
        first_name = body.get("first_name")
        last_name = body.get("last_name")
        email = body.get("email")
        password = body.get("password")
        phone_number = body.get("phone_number")
        address = body.get("address")
        profile_image_url = body.get("profile_image_url")

        system_creation_time = timezone.now()
        system_update_time = timezone.now()
        status_value = 1

        # Auto-increment manually if needed
        last_id = Employees.objects.aggregate(max_id=models.Max('id'))['max_id'] or 0
        new_id = last_id + 1

        # Uniqueness checks (ignore deleted employees)
        existing_email = Employees.objects.filter(email=email).exclude(status=5).exists()
        existing_phone = Employees.objects.filter(phone_number=phone_number).exclude(status=5).exists()

        # Field validations
        if not first_name:
            return Response({
                "status": "Error",
                "message": "Enter First Name"
            }, status=status.HTTP_409_CONFLICT)

        if not email:
            return Response({
                "status": "Error",
                "message": "Please Enter Email Address"
            }, status=status.HTTP_409_CONFLICT)

        if existing_email:
            return Response({
                "status": "Error",
                "message": "Duplicate Email Address. Please Enter a Unique one"
            }, status=status.HTTP_409_CONFLICT)

        if not password:
            return Response({
                "status": "Error",
                "message": "Please Enter Password"
            }, status=status.HTTP_409_CONFLICT)

        if not phone_number:
            return Response({
                "status": "Error",
                "message": "Please Enter Phone Number"
            }, status=status.HTTP_409_CONFLICT)

        if existing_phone:
            return Response({
                "status": "Error",
                "message": "Duplicate Phone Number. Please Enter a Unique one"
            }, status=status.HTTP_409_CONFLICT)

        if not address:
            return Response({
                "status": "Error",
                "message": "Please Enter Address"
            }, status=status.HTTP_409_CONFLICT)

        # ✅ Create employee using ORM
        hashed_password = make_password(password)
        employee = Employees.objects.create(
            id=new_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            phone_number=phone_number,
            address=address,
            profile_image_url=profile_image_url,
            system_creation_time=system_creation_time,
            system_update_time=system_update_time,
            status=status_value
        )

        serializer = EmployeesCreateSerializer(employee)
        return Response({
            "status": "OK",
            "message": "Employee created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    except json.JSONDecodeError:
        return Response({
            "status": "Error",
            "message": "Invalid JSON"
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            "status": "Error",
            "message": f"Internal Server Error: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@authentication_classes([StaticTokenAuthentication])
@permission_classes([AllowAny])
def project_create(request):
    try:
        body = json.loads(request.body.decode('utf-8'))
        allowed_fields = {"title", "description", "banner_image_url", "created_by"}
        received_fields = set(body.keys())
        invalid_fields = received_fields - allowed_fields
        if invalid_fields:
            return Response({
                "status": "Error",
                "message": f"Correct this key {', '.join(invalid_fields)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        body = request.data
        title = body.get("title")
        description = body.get("description")
        banner_image_url = body.get("banner_image_url")
        created_by = body.get("created_by")
        system_creation_time = timezone.now()
        system_update_time = timezone.now()
        status_value = 1
        print(body, title)

        # Auto-increment of ids
        last_id = Project.objects.aggregate(max_id=models.Max('id'))['max_id'] or 0
        new_id = last_id + 1
        # Uniqueness checks
        existing_title = Project.objects.filter(title=title).exclude(status=5).exists()
        print(existing_title)

        #1. Validate title with not null value and same project name
        if not title:
            return Response({
                "status": "Error",
                "message": "Enter Project Name"
            }, status=status.HTTP_409_CONFLICT)
        if existing_title:
            return Response({
                "status": "Error",
                "message": "Duplicate Project Name."
            }, status=status.HTTP_409_CONFLICT)

        project = Project.objects.create(
            id=new_id,
            title=title,
            description=description,
            banner_image_url=banner_image_url,
            system_creation_time=system_creation_time,
            system_update_time=system_update_time,
            status=status_value
        )

        serializer = ProjectCreateSerializer(project)
        return Response({
            "status": "OK",
            "message": "Employee created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({
            "status": "Error",
            "message": f"Internal Server Error: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@authentication_classes([StaticTokenAuthentication])
@permission_classes([AllowAny])
def project_list(request):
    payload = request.data
    project_id = payload.get('id')
    data_limit = payload.get('limit')
    page_no = payload.get('page')
    print(type(project_id))
    data = []

    try:
        if project_id and type(project_id) == int:
            # Fetch a single Project by ID
            try:
                emp = Project.objects.get(id=project_id)
                serializer = ProjectSerializer(emp)
                data.append(serializer.data)
                message = "Project details retrieved successfully"
            except Project.DoesNotExist:
                return Response({
                    "status": "Error",
                    "message": "Project details not found",
                    "data": []
                }, status=status.HTTP_404_NOT_FOUND)

        elif data_limit and page_no:
            project = Project.objects.all().order_by('id')
            start = (page_no - 1) * data_limit
            end = start + data_limit
            paginated_project = project[start:end]
            serializer = ProjectSerializer(paginated_project, many=True)
            data = serializer.data
            if len(data) == 0:
                return Response({
                    "status": "Error",
                    "message": "Project details not found",
                    "data": []
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                message = "Project details retrieved successfully"

        elif not payload:
            # Fetch all employees if payload is empty
            employees = Project.objects.all().order_by('id')
            serializer = ProjectSerializer(employees, many=True)
            data = serializer.data
            message = "Project details retrieved successfully"

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
            "message": "Internal Server Error:",
            "data": []
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)