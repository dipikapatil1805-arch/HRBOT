import os
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://dipikapatil1805_db_user:HRBOT@123@cluster0.qbn1m7r.mongodb.net/hrbot?retryWrites=true&w=majority&appName=Cluster0"
)
db = client["hrbot"]

employees = db["employees"]
departments = db["departments"]
attendance = db["attendance"]
leave_requests = db["leave_requests"]
payroll = db["payroll"]
leave_balance = db["leave_balance"] 
