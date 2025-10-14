from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import EmployeesTest, Employees
from django.db import models
from .serializers import EmployeesTestSerializer
from .serializers import EmployeesSerializer, EmployeesCreateSerializer
from django.utils import timezone
from django.contrib.auth.hashers import make_password

# GET all employees Details
@csrf_exempt
def employee_list(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            payload = json.loads(body) if body else {}
            print(payload)
        except json.JSONDecodeError:
            return JsonResponse({
                "status": "Error",
                "message": "Invalid JSON",
                "data": []
            }, status=400)

        emp_id = payload.get('id')
        data_limit = payload.get('limit')
        page_no = payload.get('page', 1)
        data = []

        if emp_id:
            # Fetch a single employee by ID
            try:
                emp = Employees.objects.get(id=emp_id)
                serializer = EmployeesSerializer(emp)
                data.append(serializer.data)
                message = f"Employee with retrieved successfully"
            except Employees.DoesNotExist:
                return JsonResponse({
                    "status": "Error",
                    "message": "No employee found",
                    "data": []
                }, status=404)

        elif data_limit and page_no:
            # Fetch all employees (or paginated)
            employees = Employees.objects.all().order_by('id')

            # Apply pagination if limit is provided
            if data_limit:
                try:
                    data_limit = int(data_limit)
                    page_no = int(page_no)
                    start = (page_no - 1) * data_limit
                    end = start + data_limit
                    employees = employees[start:end]
                except ValueError:
                    return JsonResponse({
                        "status": "Error",
                        "message": "limit and page must be integers",
                        "data": []
                    }, status=400)

            serializer = EmployeesSerializer(employees, many=True)
            data = serializer.data
            message = "Employees retrieved successfully"
        elif payload == {}:
            employees = Employees.objects.all().order_by('id')
            serializer = EmployeesSerializer(employees, many=True)
            data = serializer.data
            message = "Employees retrieved successfully"
        
        else:
            message = "Invalid Input"

        return JsonResponse({
            "status": "OK",
            "message": message,
            "data": data
        })

    else:
        return JsonResponse({
            "status": "Error",
            "message": "Method not allowed"
        }, status=405)
    
# POST create employee
@csrf_exempt  # disable CSRF for simplicity; better to handle CSRF in production
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
                }, status=200)
            if not email:
                return JsonResponse({
                    "status": "Error",
                    "message": "Please Enter Email Address"
                }, status=200)
            if existing_count_email>=1:
                return JsonResponse({
                    "status": "Error",
                    "message": "Duplicate Email Address Please Enter Unique one"
                }, status=200)
            if not phone_number:
                return JsonResponse({
                    "status": "Error",
                    "message": "Please Enter Phone Number"
                }, status=200)
            if existing_count_phone>=1:
                return JsonResponse({
                    "status": "Error",
                    "message": "Duplicate Phone Number Please Enter Unique one"
                }, status=200)
            if not address:
                return JsonResponse({
                    "status": "Error",
                    "message": "Please Enter Address"
                }, status=200)
            
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