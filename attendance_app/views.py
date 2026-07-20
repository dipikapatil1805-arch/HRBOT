from django.shortcuts import render, redirect
from config.mongodb import attendance


# ==========================
# Attendance List
# ==========================
def attendance_list(request):

    records = list(attendance.find())

    return render(request, "attendance/attendance_list.html", {
        "records": records
    })


# ==========================
# Add Attendance
# ==========================
def add_attendance(request):

    if request.method == "POST":

        attendance.insert_one({
            "employee_id": request.POST.get("employee_id"),
            "date": request.POST.get("date"),
            "status": request.POST.get("status")
        })

        return redirect("attendance_list")

    return render(request, "attendance/add_attendance.html")


# ==========================
# Delete Attendance
# ==========================
def delete_attendance(request, employee_id):

    attendance.delete_one({
        "employee_id": employee_id
    })

    return redirect("attendance_list")