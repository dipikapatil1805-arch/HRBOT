from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["hrbot"]

employees = db["employees"]
departments = db["departments"]
attendance = db["attendance"]
leave_requests = db["leave_requests"]
payroll = db["payroll"]
leave_balance = db["leave_balance"] 
