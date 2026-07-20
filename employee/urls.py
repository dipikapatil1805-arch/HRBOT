from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    
    path("employees/", views.employee_list, name="employee_list"),
    path("employees/add/", views.add_employee, name="add_employee"),
    path("employees/edit/<str:employee_id>/", views.edit_employee, name="edit_employee"),
    path("employees/delete/<str:employee_id>/", views.delete_employee, name="delete_employee"),
]
