from django.shortcuts import render, redirect
from config.mongodb import employees, leave_balance
from config.mongodb import attendance, leave_requests, payroll


# ==========================
# Dashboard
# ==========================
def dashboard(request):

    total_employees = employees.count_documents({})
    total_attendance = attendance.count_documents({})
    pending_leaves = leave_requests.count_documents({"status": "Pending"})
    total_payroll = payroll.count_documents({})

    context = {
        "total_employees": total_employees,
        "total_attendance": total_attendance,
        "pending_leaves": pending_leaves,
        "total_payroll": total_payroll,
    }

    return render(request, "dashboard/dashboard.html", context)


# ==========================
# Employee List + Search
# ==========================
def employee_list(request):

    search = request.GET.get("search", "").strip()

    if search:
        employee_list = list(
            employees.find({
                "$or": [
                    {"employee_id": {"$regex": search, "$options": "i"}},
                    {"first_name": {"$regex": search, "$options": "i"}},
                    {"last_name": {"$regex": search, "$options": "i"}},
                    {"department": {"$regex": search, "$options": "i"}},
                    {"designation": {"$regex": search, "$options": "i"}},
                ]
            })
        )
    else:
        employee_list = list(employees.find())

    return render(request, "employee/employee_list.html", {
        "employees": employee_list,
        "search": search,
    })


# ==========================
# Add Employee
# ==========================
def add_employee(request):

    if request.method == "POST":

        employee = {
            "employee_id": request.POST.get("employee_id"),
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "department": request.POST.get("department"),
            "designation": request.POST.get("designation"),
            "salary": request.POST.get("salary"),
            "joining_date": request.POST.get("joining_date"),
        }

        employees.insert_one(employee)

        leave_balance.insert_one({
            "employee_id": employee["employee_id"],
            "casual_leave": 12,
            "sick_leave": 10,
            "earned_leave": 15
        })

        return redirect("employee_list")

    return render(request, "employee/add_employee.html")


# ==========================
# Edit Employee
# ==========================
def edit_employee(request, employee_id):

    employee = employees.find_one({"employee_id": employee_id})

    if not employee:
        return redirect("employee_list")

    if request.method == "POST":

        updated_employee = {
            "employee_id": request.POST.get("employee_id"),
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "department": request.POST.get("department"),
            "designation": request.POST.get("designation"),
            "salary": request.POST.get("salary"),
            "joining_date": request.POST.get("joining_date"),
        }

        employees.update_one(
            {"employee_id": employee_id},
            {"$set": updated_employee}
        )

        return redirect("employee_list")

    return render(request, "employee/edit_employee.html", {
        "employee": employee
    })


# ==========================
# Delete Employee
# ==========================
def delete_employee(request, employee_id):

    employees.delete_one({"employee_id": employee_id})
    leave_balance.delete_one({"employee_id": employee_id})

    return redirect("employee_list")