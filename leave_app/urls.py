from django.urls import path
from . import views

urlpatterns = [
    path("leave/", views.leave_list, name="leave_list"),
    path("leave/apply/", views.apply_leave, name="apply_leave"),

    path("leave/approve/<str:leave_id>/", views.approve_leave, name="approve_leave"),
    path("leave/reject/<str:leave_id>/", views.reject_leave, name="reject_leave"),
    path("leave/delete/<str:leave_id>/", views.delete_leave, name="delete_leave"),
]