import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Data
employee_data = {
    "name": "John Doe",
    "role": "Manager",
    "availability": "Mon-Fri 9-5",
    "preferred_hours": 40
}

# 1. Add an Employee
def test_add_employee():
    response = requests.post(f"{BASE_URL}/employees", json=employee_data)
    print("Raw Response Content:", response.content)
    print("Response Status Code:", response.status_code)

    try:
        json_data = response.json()
        print("Add Employee Response:", json_data)
        return json_data.get('id')
    except requests.exceptions.JSONDecodeError:
        print("Error: Response is not in JSON format")
        return None

# 2. Submit a Holiday Request
def test_request_holiday(employee_id):
    data = {
        "employee_id": employee_id,
        "date": "2024-03-15"
    }
    response = requests.post(f"{BASE_URL}/holiday_requests", json=data)
    print("\nSubmit Holiday Request Response:", response.status_code, response.content)
    try:
        return response.json().get('id')
    except requests.exceptions.JSONDecodeError:
        print("Error: Response is not in JSON format")
        return None

# 3. Get All Holiday Requests
def test_get_holiday_requests():
    response = requests.get(f"{BASE_URL}/holiday_requests")
    print("\nGet All Holiday Requests Response:", response.status_code, response.content)

# 4. Approve a Holiday Request
def test_approve_holiday_request(request_id):
    data = {"status": "Approved"}
    response = requests.put(f"{BASE_URL}/holiday_requests/{request_id}", json=data)
    print("\nApprove Holiday Request Response:", response.status_code, response.content)

# 5. Get Employee's Holiday Requests
def test_get_employee_holiday_requests(employee_id):
    response = requests.get(f"{BASE_URL}/employees/{employee_id}/holiday_requests")
    print("\nGet Employee Holiday Requests Response:", response.status_code, response.content)

# Run Tests
if __name__ == "__main__":
    # Step 1: Add an employee
    employee_id = test_add_employee()
    if not employee_id:
        print("Failed to add employee.")
        exit(1)

    # Step 2: Submit a holiday request
    holiday_request_id = test_request_holiday(employee_id)
    if not holiday_request_id:
        print("Failed to submit holiday request.")
        exit(1)

    # Step 3: Get all holiday requests
    test_get_holiday_requests()

    # Step 4: Approve the holiday request
    test_approve_holiday_request(holiday_request_id)

    # Step 5: Get the employee's holiday requests
    test_get_employee_holiday_requests(employee_id)
