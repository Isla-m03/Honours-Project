# bulk_add_employees.py

import requests
import random

BASE_URL = "http://127.0.0.1:5000/employees"
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MzUyNjA5NSwianRpIjoiYzhmN2FiZWYtMmFiNy00OTAwLTliZWEtOGY3NmZkOWM1Zjc3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NDM1MjYwOTUsImNzcmYiOiJmNzRmOWIxNy1jMWE4LTRkN2MtYWI1ZS1lZmIyMzNkMmUwMDEiLCJleHAiOjE3NDM1MjY5OTV9.Rdv4YpFf4ooucPSF9Z6ZWYpuJnpyNY8e-HH7m7PyoRM"

headers = {
    "Authorization": f"Bearer {JWT_TOKEN}",
    "Content-Type": "application/json"
}

roles = ["Server", "Chef", "Bartender", "Door Host", "Server Assistant", "Manager"]

availability_options = [
    "Mon-Fri 10:00-17:00",
    "Tue-Sat 17:00-23:00",
    "Wed-Sun 10:00-23:00",
    "Mon-Wed 10:00-17:00, Fri-Sun 17:00-23:00",
    "Thu-Sat 10:00-23:00",
    "Mon-Sun 10:00-23:00"
]

names = [
    "Emily Smith", "John Doe", "Michael Johnson", "Sarah Brown", "David Jones", "Anna Davis",
    "James Wilson", "Sophia Taylor", "Chris Moore", "Jessica Anderson",
    "Daniel Thomas", "Olivia Jackson", "Ryan White", "Isabella Harris", "Matthew Martin", "Mia Thompson",
    "Kevin Garcia", "Emma Martinez", "Luke Robinson", "Ava Clark",
    "Jacob Rodriguez", "Charlotte Lewis", "Ethan Lee", "Amelia Walker", "Noah Hall",
    "Harper Allen", "Liam Young", "Evelyn King", "Mason Wright", "Luna Scott",
    "Alexander Green", "Chloe Adams", "Benjamin Baker", "Layla Gonzalez", "Elijah Nelson",
    "Zoe Carter", "Henry Mitchell", "Scarlett Perez", "Jack Roberts", "Ellie Turner"
]

for i in range(40):
    employee_data = {
        "name": names[i],
        "role": random.choice(roles),
        "availability": random.choice(availability_options),
        "preferred_hours": random.randint(5, 40)
    }

    response = requests.post(BASE_URL, json=employee_data, headers=headers)

    if response.status_code == 201:
        print(f"✅ Added: {employee_data['name']} - {employee_data['role']}")
    else:
        print(f"❌ Failed: {employee_data['name']} - {response.status_code} - {response.text}")

print("🚀 Done adding employees.")
