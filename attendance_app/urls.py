from django.urls import path
from . import views

urlpatterns = [
    path("attendance/", views.attendance_list, name="attendance_list"),
    path("attendance/add/", views.add_attendance, name="add_attendance"),
    path("attendance/delete/<str:employee_id>/", views.delete_attendance, name="delete_attendance"),
]