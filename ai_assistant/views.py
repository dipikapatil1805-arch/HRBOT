from django.shortcuts import render
from config.mongodb import employees, attendance, leave_requests, payroll


def ai_chat(request):

    response = ""

    if request.method == "POST":

        question = request.POST.get("question", "").lower()

        # Greetings
        if "hello" in question or "hi" in question:
            response = "Hello! Welcome to HRBOT. How can I help you today?"

        # Employee
        elif "employee" in question or "employees" in question:
            total = employees.count_documents({})
            response = f"There are {total} employees in the organization."

        # Attendance
        elif "attendance" in question:
            total = attendance.count_documents({})
            response = f"There are {total} attendance records."

        # Leave
        elif "leave" in question:
            total = leave_requests.count_documents({})
            response = f"There are {total} leave requests in the system."

        # Payroll
        elif "salary" in question or "payroll" in question:
            total = payroll.count_documents({})
            response = f"There are {total} payroll records available."

        # Reports
        elif "report" in question:
            response = "Reports can be downloaded as PDF and Excel from the Reports module."

        # About HRBOT
        elif "about" in question or "hrbot" in question:
            response = "HRBOT is an HR Management System developed using Django and MongoDB."

        # Thanks
        elif "thank" in question:
            response = "You're welcome! Happy to help."

        else:
            response = "Sorry, I couldn't understand your question. Please ask about employees, attendance, leave, payroll, or reports."

    return render(request, "ai/chat.html", {
        "response": response
    })