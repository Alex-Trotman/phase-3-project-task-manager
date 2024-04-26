# lib/helpers.py

from models.project import Project
from models.task import Task


def exit_program():
    print("Goodbye!")
    exit()

def list_departments():
    departments = Department.get_all()
    for department in departments:
        print(department)


def find_department_by_name():
    name = input("Enter the department's name: ")
    department = Department.find_by_name(name)
    print(department) if department else print(
        f'Department {name} not found')


def find_department_by_id():
    # use a trailing underscore not to override the built-in id function
    id_ = input("Enter the department's id: ")
    department = Department.find_by_id(id_)
    print(department) if department else print(f'Department {id_} not found')


def create_department():
    name = input("Enter the department's name: ")
    location = input("Enter the department's location: ")
    try:
        department = Department.create(name, location)
        print(f'Success: {department}')
    except Exception as exc:
        print("Error creating department: ", exc)


def update_department():
    id_ = input("Enter the department's id: ")
    if department := Department.find_by_id(id_):
        try:
            name = input("Enter the department's new name: ")
            department.name = name
            location = input("Enter the department's new location: ")
            department.location = location

            department.update()
            print(f'Success: {department}')
        except Exception as exc:
            print("Error updating department: ", exc)
    else:
        print(f'Department {id_} not found')


def delete_department():
    id_ = input("Enter the department's id: ")
    if department := Department.find_by_id(id_):
        department.delete()
        print(f'Department {id_} deleted')
    else:
        print(f'Department {id_} not found')


# You'll implement the employee functions in the lab

def list_employees():
    employees = Employee.get_all()
    for employee in employees:
        print(employee)


def find_employee_by_name():
    name = input("Enter the employee's name: ")
    employee = Employee.find_by_name(name)
    print(employee) if employee else print(
        f'Employee {name} not found')


def find_employee_by_id():
    id_ = input("Enter the employee's id: ")
    employee = Employee.find_by_id(id_)
    print(employee) if employee else print(f'Employee {id_} not found')


def create_employee():
    name = input("Enter the employee's name: ")
    job_title = input("Enter the employee's location: ")
    department_id = input("Enter the employee's department id: ")
    print(type(department_id))

    department = Department.find_by_id(department_id)
    print(department)
    if not department:
        print(f"Error: Department with ID {department_id} does not exist.")
        return

    try:
        employee = Employee.create(name, job_title, int(department_id))
        print(f'Success: {employee}')
    except Exception as exc:
        print("Error creating employee: ", exc)


def update_employee():
    id_ = input("Enter the Employee's id: ")
    if employee := Employee.find_by_id(id_):
        try:
            name = input("Enter the Employee's new name: ")
            employee.name = name
            location = input("Enter the Employee's new job_title: ")
            employee.job_title = location

            employee.update()
            print(f'Success: {employee}')
        except Exception as exc:
            print("Error updating employee: ", exc)
    else:
        print(f'Employee {id_} not found')


def delete_employee():
    id_ = input("Enter the employee's id: ")
    if employee := Employee.find_by_id(id_):
        employee.delete()
        print(f'Employee {id_} deleted')
    else:
        print(f'Employee {id_} not found')


def list_department_employees():
    department_id = input("Enter the department's id: ")
    department = Department.find_by_id(department_id)
    
    if department:
        print(f"Listing employees for Department {department_id}: {department.name}")
        employees = department.employees()  # Assuming this method correctly retrieves the associated employees
        if employees:
            for employee in employees:
                print(employee)
        else:
            print("No employees found in this department.")
    else:
        print(f"Department with ID {department_id} not found")