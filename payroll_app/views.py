from django.shortcuts import render, redirect
from bson import ObjectId
from config.mongodb import db

payroll_collection = db["payroll"]

def payroll_list(request):
    payrolls = list(payroll_collection.find())

    for payroll in payrolls:
        payroll["id"] = str(payroll["_id"])

    return render(request, "payroll/payroll_list.html", {
        "payrolls": payrolls
    })

def add_payroll(request):

    if request.method == "POST":

        basic_salary = float(request.POST.get("basic_salary"))
        bonus = float(request.POST.get("bonus"))
        deduction = float(request.POST.get("deduction"))

        net_salary = basic_salary + bonus - deduction

        payroll = {
            "emp_id": request.POST.get("emp_id"),
            "emp_name": request.POST.get("emp_name"),
            "basic_salary": basic_salary,
            "bonus": bonus,
            "deduction": deduction,
            "net_salary": net_salary,
            "month": request.POST.get("month"),
        }

        payroll_collection.insert_one(payroll)

        return redirect("payroll_list")

    return render(request, "payroll/add_payroll.html")
def edit_payroll(request, id):
    payroll = payroll_collection.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        payroll_collection.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "emp_id": request.POST.get("emp_id"),
                    "emp_name": request.POST.get("emp_name"),
                    "basic_salary": request.POST.get("basic_salary"),
                    "bonus": request.POST.get("bonus"),
                    "deduction": request.POST.get("deduction"),
                    "net_salary": request.POST.get("net_salary"),
                    "month": request.POST.get("month"),
                }
            }
        )
        return redirect("payroll_list")

    return render(request, "payroll/edit_payroll.html", {
        "payroll": payroll
    })


def delete_payroll(request, id):
    payroll_collection.delete_one({"_id": ObjectId(id)})
    return redirect("payroll_list")