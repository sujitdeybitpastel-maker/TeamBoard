from django.urls import path
from . import views

urlpatterns = [
    path('employee_test/', views.employee_list_test, name='employee-list'),
    path('employee_test/create/', views.employee_create_test, name='employee-create'),
    path('employee/', views.employee_list, name='employee-list'),
    #path('employee/create/', views.employee_create, name='employee-create'),
]


