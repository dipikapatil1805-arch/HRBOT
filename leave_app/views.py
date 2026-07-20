from django.shortcuts import render, redirect
from config.mongodb import leave_requests, leave_balance


# =========================
# Leave List
# =========================
def leave_list(request):

    leaves = list(leave_requests.find())

    for leave in leaves:
        leave["id"] = str(leave["_id"])

    return render(request, "leave/leave_list.html", {
        "leaves": leaves
    })


# =========================
# Apply Leave
# =========================
def apply_leave(request):

    if request.method == "POST":

        print("POST request received")

        employee_id = request.POST.get("employee_id")
        print("Employee:", employee_id)

        balance = leave_balance.find_one({
            "employee_id": employee_id
        })

        print("Balance:", balance)

        leave = {
            "employee_id": employee_id,
            "leave_type": request.POST.get("leave_type"),
            "from_date": request.POST.get("from_date"),
            "to_date": request.POST.get("to_date"),
            "reason": request.POST.get("reason"),
            "status": "Pending"
        }

        result = leave_requests.insert_one(leave)

        print("Inserted ID:", result.inserted_id)

        return redirect("leave_list")

    return render(request, "leave/apply_leave.html")
# =========================
# Approve Leave
# ========================= 
from bson import ObjectId

def approve_leave(request, leave_id):

    print("Leave ID:", leave_id)

    leave = leave_requests.find_one({"_id": ObjectId(leave_id)})
    print("Leave:", leave)

    if not leave:
        print("Leave NOT found")
        return redirect("leave_list")

    balance = leave_balance.find_one({
        "employee_id": leave["employee_id"]
    })
    print("Balance:", balance)

    if not balance:
        print("Balance NOT found")
        return redirect("leave_list")

    mapping = {
        "Casual Leave": "casual_leave",
        "Sick Leave": "sick_leave",
        "Paid Leave": "earned_leave",
        "casual_leave": "casual_leave",
        "sick_leave": "sick_leave",
        "earned_leave": "earned_leave",
    }

    field = mapping.get(leave["leave_type"])

    print("Field:", field)
    print("Current Balance:", balance.get(field))

    result = leave_requests.update_one(
        {"_id": ObjectId(leave_id)},
        {"$set": {"status": "Approved"}}
    )

    print("Matched:", result.matched_count)
    print("Modified:", result.modified_count)

    leave_balance.update_one(
        {"employee_id": leave["employee_id"]},
        {"$inc": {field: -1}}
    )

    return redirect("leave_list")
# =========================
# Reject Leave
# =========================
def reject_leave(request, leave_id):

    leave_requests.update_one(
        {"_id": ObjectId(leave_id)},
        {"$set": {"status": "Rejected"}}
    )

    return redirect("leave_list")

# =========================
# Delete Leave
# =========================
def delete_leave(request, leave_id):

    leave_requests.delete_one(
        {"_id": ObjectId(leave_id)}
    )

    return redirect("leave_list")
