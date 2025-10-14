from django.urls import path
from . import views

urlpatterns = [
    path('employee/', views.employee_list, name='employee-list'),
    path('employee/create/', views.employee_create, name='employee-create'),
]


