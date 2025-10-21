from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.employees_list, name='employees-list'),
    path('employee/', views.employee_list, name='employees-list'),
    path('employee/create/', views.employee_create, name='employee-create'),
    path('project/create/', views.project_create, name='project-create'),
    path('projects/', views.projects_list, name='projects-list'),
    path('project/', views.project_list, name='project-list'),
    path('project/add_member/', views.project_add_member, name='project-add-member'),
    path('test/add/', views.test_add, name='test-add'),
    path('project/remove_member/', views.project_remove_member, name='project_remove_member'),
    path('project/members/', views.project_members_list, name='project_member'),
    path('project/message/', views.project_message, name='project-message'),
    
]
