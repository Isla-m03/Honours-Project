import requests
import json

BASE_URL = "http://127.0.0.1:5000/employees"

# Test Data
employee_data = {
    "name": "John Doe",
    "role": "Manager",
    "availability": "Mon-Fri 9-5",
    "preferred_hours": 40
}

# 1. Add an Employee
def test_add_employee():
    response = requests.post(BASE_URL, json=employee_data)
    print("Add Employee Response:")
    print(response.status_code, response.json())

# 2. Get All Employees
def test_get_employees():
    response = requests.get(BASE_URL)
    print("\nGet All Employees Response:")
    print(response.status_code, response.json())

# 3. Get a Single Employee by ID
def test_get_employee(employee_id):
    response = requests.get(f"{BASE_URL}/{employee_id}")
    print(f"\nGet Employee {employee_id} Response:")
    print(response.status_code, response.json())

# 4. Update an Employee
def test_update_employee(employee_id):
    updated_data = {
        "name": "Jane Doe",
        "preferred_hours": 35
    }
    response = requests.put(f"{BASE_URL}/{employee_id}", json=updated_data)
    print(f"\nUpdate Employee {employee_id} Response:")
    print(response.status_code, response.json())

# 5. Delete an Employee
def test_delete_employee(employee_id):
    response = requests.delete(f"{BASE_URL}/{employee_id}")
    print(f"\nDelete Employee {employee_id} Response:")
    print(response.status_code, response.json())

# Run Tests
if __name__ == "__main__":
    # Start with adding an employee
    test_add_employee()

    # Get all employees
    test_get_employees()

    # Assume the first employee has ID = 1 (adjust if needed)
    employee_id = 1

    # Get details of a single employee
    test_get_employee(employee_id)

    # Update the employee
    test_update_employee(employee_id)

    # Get all employees after the update
    test_get_employees()

    # Delete the employee
    test_delete_employee(employee_id)

    # Get all employees after deletion
    test_get_employees()
