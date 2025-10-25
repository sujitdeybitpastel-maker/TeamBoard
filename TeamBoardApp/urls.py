from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.employees_list, name='employees-list'), # Updated time null when it insert the database
    path('employee/', views.employee_list, name='employee-list'),
    path('employee/create/', views.employee_create, name='employee-create'),
    path('project/create/', views.project_create, name='project-create'),
    path('projects/', views.projects_list, name='projects-list'),
    path('project/', views.project_list, name='project-list'),
    path('project/add_member/', views.project_add_member, name='project-add-member'), #Implement here md5
    path('test/add/', views.test_add, name='test-add'),
    path('project/remove_member/', views.project_remove_member, name='project_remove_member'),# Implement Here md5
    path('project/members/', views.project_members_list, name='project_member'), # Implement Here md5
    path('project/message/', views.project_message, name='project-message'), # Send a message in a project.
    path('project/messages/', views.project_messages, name='project-messages'), # Fetch all messages in a project.
    path('employee/messages/', views.employee_messages, name='employee-messages'), # Fetch all messages in a project.
    #https://teamboard-pyi4.onrender.com/employee
]
