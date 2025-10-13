from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import EmployeesTest, Employees
from django.db import models



@csrf_exempt  # Disable CSRF for simplicity
def employee_list_test(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            print("----------------Body-------------",body)
            payload = json.loads(body) if body else {}
            print("----------------payload-------------",payload)

        except json.JSONDecodeError:
            return JsonResponse({
                "status": "Error",
                "message": "Invalid JSON",
                "data": []
            }, status=400)
        
        emp_id = payload.get('id')
        data_limit = payload.get("limit")
        page_no = payload.get("page")
        print(data_limit,page_no)
        data = []

        if emp_id:
            # Fetch a single employee by ID
            try:
                emp = EmployeesTest.objects.get(id=emp_id)
                data.append({
                    "id": emp.id,
                    "first_name": emp.f_name,
                    "last_name": emp.l_name,
                    "email": emp.email
                })
                message = f"Employee with id {emp_id} retrieved successfully"
            except EmployeesTest.DoesNotExist:
                return JsonResponse({
                    "status": "Error",
                    "message": f"No employee found with id {emp_id}",
                    "data": []
                }, status=404)
        elif data_limit:
            start = (page_no - 1) * data_limit  # (1-1)*10 = 0
            end = start + data_limit           # 0+10 = 10
            employees = EmployeesTest.objects.all().order_by('id')[start:end] 
            for emp in employees:
                data.append({
                    "id": emp.id,
                    "first_name": emp.f_name,
                    "last_name": emp.l_name,
                    "email": emp.email
                })
            message = "Employees Pagination retrieved successfully"

        else:
            # Fetch all employees
            employees = EmployeesTest.objects.all()
            for emp in employees:
                data.append({
                    "id": emp.id,
                    "first_name": emp.f_name,
                    "last_name": emp.l_name,
                    "email": emp.email
                })
            message = "Employees retrieved successfully"

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
def employee_create_test(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            first_name = body.get("first_name")
            last_name = body.get("last_name")
            email = body.get("email")
            last_id = EmployeesTest.objects.aggregate(max_id=models.Max('id'))['max_id'] or 0
            new_id = last_id + 1

            print('------------------------',first_name)

            if not all([first_name, last_name, email]):
                return JsonResponse({
                    "status": "Error",
                    "message": "Missing fields"
                }, status=400)

            # create employee using ORM
            employee = EmployeesTest.objects.create(
                id = new_id,
                f_name=first_name,
                l_name=last_name,
                email=email
            )

            return JsonResponse({
                "status": "OK",
                "message": "Employee created successfully",
                "data": {
                    "id": employee.id,
                    "first_name": employee.f_name,
                    "last_name": employee.l_name,
                    "email": employee.email
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({
                "status": "Error",
                "message": "Invalid JSON"
            }, status=400)




# GET all employees Details
def employee_list(request):
    if request.method == 'GET':
        employees = Employees.objects.all()
        data = []
        for emp in employees:
            data.append({
                "id": emp.id,
                "first_name": emp.first_name,
                "last_name": emp.last_name,
                "email": emp.email,
                "phone_number": emp.phone_number,
                "address":emp.address,
                "profile_image_url":emp.profile_image_url,
                "status":emp.status



            })
        return JsonResponse({
            "status": "OK",
            "message": "Employees retrieved successfully",
            "data": data
        })