from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
import json
from .models import Employees, Project,ProjectMembership,Status,TableTestingEnumData
from django.db import models
from .serializers import EmployeesSerializer, EmployeesCreateSerializer,ProjectCreateSerializer,ProjectSerializer,AddMemberSerializer,RemoveMemberSerializer,ProjectMemberSerializer,ProjectMemberSerializer
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from .authentication import StaticTokenAuthentication
from django.db.models.functions import Cast
from django.db.models import IntegerField
from django.shortcuts import get_object_or_404

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
        if emp_id and type(emp_id) == int:
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
            # try:
            #     data_limit = int(data_limit)
            #     page_no = int(page_no)
            # except ValueError:
            #     return Response({
            #         "status": "Error",
            #         "message": "limit and page must be integers",
            #         "data": []
            #     }, status=status.HTTP_400_BAD_REQUEST)

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
                "message": "Invalid Payload",
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
    # 1. Trim the values of f_name, l_name, address
    # 2. Validate email address/Phone number
    # 3. Validate all required field for Null value - Done
    # 4. Validate payload keys - Done 
    try:
        body = json.loads(request.body.decode('utf-8'))
        allowed_fields = {"first_name", "last_name", "email", "password","phone_number","address","profile_image_url"}
        received_fields = set(body.keys())
        invalid_fields = received_fields - allowed_fields
        if invalid_fields:
            return Response({
                "status": "Error",
                "message": "Invalid Payload"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        payload = request.data
        cleaned_data = {k: v.strip() if isinstance(v, str) else v for k, v in payload.items()}
        print(payload)
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        phone_number = cleaned_data.get("phone_number")
        address = cleaned_data.get("address")
        profile_image_url = cleaned_data.get("profile_image_url")
        system_creation_time = timezone.now()
        system_update_time = timezone.now()
        # status_value = 1
        
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
            system_update_time=system_update_time
            # status=status_value
        )

        serializer = EmployeesCreateSerializer(employee)
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
def project_create(request):
    try:
        body = json.loads(request.body.decode('utf-8'))
        allowed_fields = {"title", "description", "banner_image_url", "created_by"}
        received_fields = set(body.keys())
        invalid_fields = received_fields - allowed_fields
        if invalid_fields:
            return Response({
                "status": "Error",
                "message": "Invalid Payload"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        body = request.data
        # # Trim Data For "   " this pattern
        # cleaned_data = {
        #     k: ("" if isinstance(v, str) and v.strip() == "" else v)
        #     for k, v in body.items()
        # }
        # Trim all string fields
        cleaned_data = {k: v.strip() if isinstance(v, str) else v for k, v in body.items()}
        title = cleaned_data.get("title")
        description = cleaned_data.get("description")
        banner_image_url = cleaned_data.get("banner_image_url")
        #created_by = cleaned_data.get("created_by")
        system_creation_time = timezone.now()
        system_update_time = timezone.now()
        # status_value = 1
        print(cleaned_data, len(title))


        # Auto-increment of ids
        last_id = Project.objects.aggregate(max_id=models.Max('id'))['max_id'] or 0
        new_id = last_id + 1
        # Uniqueness checks
        existing_title = Project.objects.annotate(
            status_int=Cast('status', IntegerField())
        ).filter(title=title).exclude(status_int=5).exists()
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
                "message": "Duplicate Project Name"
            }, status=status.HTTP_409_CONFLICT)

        project = Project.objects.create(
            id=new_id,
            title=title,
            description=description,
            banner_image_url=banner_image_url,
            system_creation_time=system_creation_time,
            system_update_time=system_update_time
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
                print("-----------------emp---------------",emp)
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
            "message": f"Internal Server Error: {str(e)}",
            "data": []
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@authentication_classes([StaticTokenAuthentication])
@permission_classes([AllowAny])
def project_add_member(request):
    try:
        body = json.loads(request.body.decode('utf-8'))
        allowed_fields = {"project_id", "member_id", "is_admin"}
        received_fields = set(body.keys())
        invalid_fields = received_fields - allowed_fields
        if invalid_fields:
            return Response({
                "status": "Error",
                "message": "Invalid Payload"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        payload = request.data
        # # Trim Data For "   " this pattern
        # cleaned_data = {
        #     k: ("" if isinstance(v, str) and v.strip() == "" else v)
        #     for k, v in body.items()
        # }
        # Trim all string fields
        cleaned_data = {k: v.strip() if isinstance(v, str) else v for k, v in payload.items()}
        project_id = cleaned_data.get('project_id')
        member_id = cleaned_data.get('member_id')
        is_admin = cleaned_data.get('is_admin')
        print(project_id,member_id,is_admin)
        #created_by = cleaned_data.get("created_by")
        system_creation_time = timezone.now()
        system_update_time = timezone.now()
        status_value = 1
        print(cleaned_data)


        # Auto-increment of ids
        last_id = ProjectMembership.objects.aggregate(max_id=models.Max('id'))['max_id'] or 0
        new_id = last_id + 1
        # Uniqueness checks
        existing_member = ProjectMembership.objects.annotate(
            status_int=Cast('status', IntegerField())
        ).filter(
            project_id=project_id,
            employees_id=member_id
        ).exclude(status_int=5).exists()
        print("---------------existing_member--------------",existing_member)

        if existing_member:
            return Response({
                "status": "Error",
                "message": "Duplicate Member"
            }, status=status.HTTP_409_CONFLICT)
        #1. project_id and member_id not null value
        if not project_id:
            return Response({
                "status": "Error",
                "message": "Enter Project ID"
            }, status=status.HTTP_409_CONFLICT)
        if not member_id:
            return Response({
                "status": "Error",
                "message": "Enter Member ID"
            }, status=status.HTTP_409_CONFLICT)

        member_create = ProjectMembership.objects.create(
            id=new_id,
            project_id=project_id,
            employees_id=member_id,
            is_admin=is_admin,
            system_creation_time=system_creation_time,
            system_update_time=system_update_time,
            status=status_value
        )

        serializer = AddMemberSerializer(member_create)
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
def test_add(request):

    try:
        body = json.loads(request.body.decode('utf-8'))
        cleaned_data = {k: v.strip() if isinstance(v, str) else v for k, v in body.items()}
        id = cleaned_data.get("id")
        #status_value = 10


        # Auto-increment of ids
        last_id = TableTestingEnumData.objects.aggregate(max_id=models.Max('id'))['max_id'] or 0
        new_id = last_id + 1
        project = TableTestingEnumData.objects.create(
            id=new_id,
            #status=status_value
        )
        return Response({
            "status": "OK"
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({
            "status": "Error",
            "message": f"Internal Server Error: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['POST'])
@authentication_classes([StaticTokenAuthentication])
@permission_classes([AllowAny])
def project_remove_member(request):

    try:
        body = json.loads(request.body.decode('utf-8'))
        allowed_fields = {"project_id", "member_id"}
        received_fields = set(body.keys())
        invalid_fields = received_fields - allowed_fields
        if invalid_fields:
            return Response({
                "status": "Error",
                "message": "Invalid Payload",
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        payload = request.data
        # # Trim Data For "   " this pattern
        # cleaned_data = {
        #     k: ("" if isinstance(v, str) and v.strip() == "" else v)
        #     for k, v in body.items()
        # }
        # Trim all string fields
        cleaned_data = {k: v.strip() if isinstance(v, str) else v for k, v in payload.items()}
        project_id = cleaned_data.get('project_id')
        member_id = cleaned_data.get('member_id')
        print(project_id,member_id)
        #created_by = cleaned_data.get("created_by")
        #system_creation_time = timezone.now()
        print(cleaned_data)


        # # Auto-increment of ids
        # last_id = ProjectMembership.objects.aggregate(max_id=models.Max('id'))['max_id'] or 0
        # new_id = last_id + 1
        # # Uniqueness checks
        existing_project = Project.objects.annotate(
            status_int=Cast('status', IntegerField())
        ).filter(
            id=project_id,
        ).exclude(status_int=5).exists()
        print("---------------existing_project--------------",existing_project)
        existing_empoyee = Employees.objects.filter(id=member_id).exclude(status=5).exists()
        print("---------------existing_empoyee--------------",existing_empoyee)
        #1. project_id and member_id not null value
        if not project_id:
            return Response({
                "status": "Error",
                "message": "Enter Project ID",
                "data": {}
            }, status=status.HTTP_409_CONFLICT)
        if not member_id:
            return Response({
                "status": "Error",
                "message": "Enter Member ID",
                "data": {}
            }, status=status.HTTP_409_CONFLICT)
        
        member_delete = ProjectMembership.objects.annotate(
            status_int=Cast('status', IntegerField())
        ).filter(
            project_id=project_id,
            employees_id=member_id
        ).exclude(status_int=5).first()  # returns object or None

        if member_delete:
            member_delete.status = '5'  # cast back to string if status is CharField
            member_delete.save()

            serializer = RemoveMemberSerializer(member_delete)
            return Response({
                "status": "OK",
                "message": "Member removed successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status": "Error",
                "message": "Member or Project is Missing",
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({
            "status": "Error",
            "message": f"Internal Server Error: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@authentication_classes([StaticTokenAuthentication])
@permission_classes([AllowAny])
def project_members_list(request):
    payload = request.data
    project_id = payload.get('project_id')
    data_limit = payload.get('limit')
    page_no = payload.get('page')
    print(project_id)
    data = []

    try:
        if project_id and type(project_id) == int:
            # Fetch all active (non-deleted) memberships
            memberships = ProjectMembership.objects.annotate(
                status_int=Cast('status', IntegerField())
            ).filter(project_id=project_id).exclude(status_int=5)  # Use '5' if status is CharField

            if not memberships.exists():
                return Response({
                    "status": "Error",
                    "message": "No members found for this project",
                    "data": []
                }, status=status.HTTP_404_NOT_FOUND)

            # Serialize the memberships
            serializer = ProjectMemberSerializer(memberships, many=True)
            data = serializer.data

            return Response({
                "status": "OK",
                "message": "Project members retrieved successfully",
                "data": data
            }, status=status.HTTP_200_OK)
        
        elif data_limit and page_no:
            memberships = ProjectMembership.objects.all().order_by('id')
            start = (page_no - 1) * data_limit
            end = start + data_limit
            paginated_memberships = memberships[start:end]
            serializer = ProjectMemberSerializer(paginated_memberships, many=True)
            data = serializer.data
            if len(data) == 0:
                return Response({
                    "status": "Error",
                    "message": "Project details not found",
                    "data": []
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                message = "Project members retrieved successfully"
        elif not payload:
            # Fetch all employees if payload is empty
            memberships = ProjectMembership.objects.all().order_by('id')
            serializer = ProjectMemberSerializer(memberships, many=True)
            data = serializer.data
            message = "Project details retrieved successfully"
        return Response({
            "status": "OK",
            "message": message,
            "data": data
        }, status=status.HTTP_200_OK)
    



    except Exception as e:
        return Response({
            "status": "Error",
            "message": f"Internal Server Error: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)