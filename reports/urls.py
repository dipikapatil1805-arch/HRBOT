from django.urls import path
from . import views

urlpatterns = [
    path("", views.report_dashboard, name="report_dashboard"),

    path("pdf/", views.export_pdf, name="export_pdf"),
    path("excel/", views.export_excel, name="export_excel"),
]