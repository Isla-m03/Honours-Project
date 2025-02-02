import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# Test Employee Data
employee_data = {
    "name": "John Doe",
    "role": "Manager",
    "availability": "Mon-Fri 9-5",
    "preferred_hours": 40
}

# 1. Add an Employee
def test_add_employee():
    response = requests.post(f"{BASE_URL}/employees", json=employee_data)
    print("Raw Response Content:", response.content)  # Print raw response
    print("Response Status Code:", response.status_code)  # Print status code

    try:
        json_data = response.json()  # Attempt to parse JSON
        print("Parsed JSON Response:", json_data)
        return json_data.get("employee", {}).get("id", 1)  # Get employee ID
    except requests.exceptions.JSONDecodeError:
        print("Error: Response is not in JSON format")
        return None

# 2. Get All Employees
def test_get_employees():
    response = requests.get(f"{BASE_URL}/employees")
    print("\nGet All Employees Response:")
    print(response.status_code, response.json())

# 3. Get a Single Employee by ID
def test_get_employee(employee_id):
    response = requests.get(f"{BASE_URL}/employees/{employee_id}")
    print(f"\nGet Employee {employee_id} Response:")
    print(response.status_code, response.json())

# 4. Update an Employee
def test_update_employee(employee_id):
    updated_data = {
        "name": "Jane Doe",
        "preferred_hours": 35
    }
    response = requests.put(f"{BASE_URL}/employees/{employee_id}", json=updated_data)
    print(f"\nUpdate Employee {employee_id} Response:")
    print(response.status_code, response.json())

# 5. Delete an Employee
def test_delete_employee(employee_id):
    response = requests.delete(f"{BASE_URL}/employees/{employee_id}")
    print(f"\nDelete Employee {employee_id} Response:")
    print(response.status_code, response.json())

# 6. Submit a Holiday Request
def test_request_holiday(employee_id):
    data = {
        "employee_id": employee_id,
        "date": "2024-03-15"
    }
    response = requests.post(f"{BASE_URL}/holiday_requests", json=data)
    print("\nSubmit Holiday Request:")
    print(response.status_code, response.json())
    return response.json().get("id", 1)  # Default to 1 if ID is missing

# 7. Get All Holiday Requests
def test_get_holiday_requests():
    response = requests.get(f"{BASE_URL}/holiday_requests")
    print("\nGet Holiday Requests:")
    print(response.status_code, response.json())

# 8. Approve a Holiday Request
def test_approve_holiday_request(request_id):
    update_data = {"status": "Approved"}
    response = requests.put(f"{BASE_URL}/holiday_requests/{request_id}", json=update_data)
    print(f"\nApprove Holiday Request {request_id}:")
    print(response.status_code, response.json())

# 9. Get an Employee’s Holiday Requests
def test_get_employee_holiday_requests(employee_id):
    response = requests.get(f"{BASE_URL}/employees/{employee_id}/holiday_requests")
    print(f"\nEmployee {employee_id} Holiday Requests:")
    print(response.status_code, response.json())

# Run Tests
if __name__ == "__main__":
    # Step 1: Add an employee
    employee_id = test_add_employee()

    # Step 2: Get all employees
    test_get_employees()

    # Step 3: Get details of a single employee
    test_get_employee(employee_id)

    # Step 4: Update the employee
    test_update_employee(employee_id)

    # Step 5: Get all employees after the update
    test_get_employees()

    # Step 6: Submit a holiday request
    holiday_request_id = test_request_holiday(employee_id)

    # Step 7: Get all holiday requests
    test_get_holiday_requests()

    # Step 8: Approve the holiday request
    test_approve_holiday_request(holiday_request_id)

    # Step 9: Get holiday requests for the employee
    test_get_employee_holiday_requests(employee_id)

    # Step 10: Delete the employee
    test_delete_employee(employee_id)

    # Step 11: Get all employees after deletion
    test_get_employees()
