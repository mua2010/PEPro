import json
import os
from homepage.models import Employee, Company


def insert_employees(json_file_name):
    '''
    Loads the JSON in json_file_name and inserts all the employees and companies into the database tables
    '''
    
    with open(json_file_name, "r") as employees_json_file:
        employees_json = json.load(employees_json_file)

    companies_dict = {}
    for employee_json in employees_json:
        companies_dict[employee_json["companyId"]] = employee_json["companyName"]

    # Insert Companies into database
    for company_id in companies_dict:
        company_name = companies_dict[company_id]
        company = Company.objects.create(
            company_id=company_id,
            company_name=company_name
        )
        companies_dict[company_id] = company

    # Insert Employees into database
    for employee_json in employees_json:
        email = employee_json["email"]
        employee_id = employee_json["employeeId"]
        first_name = employee_json["firstName"]
        last_name = employee_json["lastName"]
        # The CEO doens't have a manager ID
        if "managerId" in employee_json:
            manager_id = employee_json["managerId"]
        else:
            manager_id = None
        company = employee_json["companyId"]
        Employee.objects.create(
            email=email,
            employee_id=employee_id,
            first_name=first_name,
            last_name=last_name,
            manager_id=manager_id,
            company=companies_dict[company_id]
        )
