from django.shortcuts import render
from config.mongodb import employees, attendance, leave_requests, payroll
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from openpyxl import Workbook


def report_dashboard(request):

    total_employees = employees.count_documents({})
    total_attendance = attendance.count_documents({})
    total_leave = leave_requests.count_documents({})
    total_payroll = payroll.count_documents({})

    context = {
        "total_employees": total_employees,
        "total_attendance": total_attendance,
        "total_leave": total_leave,
        "total_payroll": total_payroll,
    }

    return render(request, "reports/report_dashboard.html", context)
def export_pdf(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="HR_Report.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold",18)
    p.drawString(180,800,"HRBot Report")

    p.setFont("Helvetica",12)

    p.drawString(100,740,f"Total Employees : {employees.count_documents({})}")
    p.drawString(100,720,f"Attendance Records : {attendance.count_documents({})}")
    p.drawString(100,700,f"Leave Requests : {leave_requests.count_documents({})}")
    p.drawString(100,680,f"Payroll Records : {payroll.count_documents({})}")

    p.save()

    return response

def export_excel(request):

    workbook = Workbook()

    sheet = workbook.active
    sheet.title = "HR Report"

    sheet.append(["Category","Count"])

    sheet.append(["Employees", employees.count_documents({})])
    sheet.append(["Attendance", attendance.count_documents({})])
    sheet.append(["Leave", leave_requests.count_documents({})])
    sheet.append(["Payroll", payroll.count_documents({})])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = 'attachment; filename="HR_Report.xlsx"'

    workbook.save(response)

    return response