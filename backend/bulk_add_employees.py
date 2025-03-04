import requests
import random

BASE_URL = "http://127.0.0.1:5000/employees"

# 🏢 Roles available in the restaurant
roles = ["Server", "Chef", "Bartender", "Door Host", "Server Assistant"]

# ⏰ Different availability patterns
availability_options = [
    "Mon-Fri 10:00-17:00",
    "Tue-Sat 17:00-23:00",
    "Wed-Sun 10:00-23:00",
    "Mon-Wed 10:00-17:00, Fri-Sun 17:00-23:00",
    "Thu-Sat 10:00-23:00",
    "Mon-Sun 12:00-20:00"
]

# 🧑‍🍳 Generate 40+ unique employee names
names = [
    "Emily", "John", "Michael", "Sarah", "David", "Anna", "James", "Sophia", "Chris", "Jessica",
    "Daniel", "Olivia", "Ryan", "Isabella", "Matthew", "Mia", "Kevin", "Emma", "Luke", "Ava",
    "Jacob", "Charlotte", "Ethan", "Amelia", "Noah", "Harper", "Liam", "Evelyn", "Mason", "Luna",
    "Alexander", "Chloe", "Benjamin", "Layla", "Elijah", "Zoe", "Henry", "Scarlett", "Jack", "Ellie"
]

# 🔄 Loop to add employees
for i in range(40):  # Adjust the number of employees as needed
    employee_data = {
        "name": names[i],  # Unique name
        "role": random.choice(roles),
        "availability": random.choice(availability_options),
        "preferred_hours": random.randint(20, 40)  # Random between 20-40 hours/week
    }

    response = requests.post(BASE_URL, json=employee_data)

    if response.status_code == 201:
        print(f"✅ Successfully added: {employee_data['name']} ({employee_data['role']})")
    else:
        print(f"❌ Failed to add {employee_data['name']} - {response.json()}")

print("🎉 All employees added!")
