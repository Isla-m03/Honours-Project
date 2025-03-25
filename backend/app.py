from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import traceback
from datetime import datetime, timedelta

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

print("Flask app is starting")

# Database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'scheduler.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)  # e.g., Server, Chef, Bartender
    availability = db.Column(db.Text, nullable=False)  # e.g., "Mon-Fri 10:00-23:00"
    preferred_hours = db.Column(db.Integer, nullable=False)  # Weekly target hours

class HolidayRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="Pending")
    employee = db.relationship('Employee', backref=db.backref('holiday_requests', lazy=True))

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    shift_type = db.Column(db.String(50), nullable=False)  # AM or PM
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)  # Assigned employee
    role = db.Column(db.String(50), nullable=False)  # Role required (Server, Chef, etc.)

    employee = db.relationship('Employee', backref=db.backref('shifts', lazy=True))

class Forecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    revenue = db.Column(db.Integer, nullable=False)  # Predicted revenue for the day

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Define required staff per revenue forecast
def get_required_staff(revenue):
    if revenue < 1000:
        return {"Server": 1, "Chef": 2, "Manager": 1}
    elif revenue < 3000:
        return {"Server": 3, "Chef": 3, "Bartender": 1, "Manager": 1}
    elif revenue < 5000:
        return {"Server": 5, "Chef": 5, "Bartender": 1, "Server Assistant": 1, "Door Host": 1, "Manager": 2}
    elif revenue < 8000:
        return {"Server": 7, "Chef": 5, "Bartender": 2, "Server Assistant": 2, "Door Host": 1, "Manager": 3}
    else:
        return {"Server": 10, "Chef": 7, "Bartender": 2, "Server Assistant": 3, "Door Host": 2, "Manager": 3}

def generate_schedule(start_date, end_date):
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        employees = Employee.query.all()
        print(f"Employees Found: {len(employees)}")

        current_date = start_date
        while current_date <= end_date:
            forecast = Forecast.query.filter_by(date=current_date).first()
            if not forecast:
                print(f"No forecast found for {current_date}, skipping...")
                current_date += timedelta(days=1)
                continue

            # Remove old shifts before generating new ones
            Shift.query.filter_by(date=current_date).delete()
            db.session.commit()
            print(f"Deleted old shifts for {current_date}")

            required_staff = get_required_staff(forecast.revenue)
            print(f"{current_date}: Initial Staffing Needs: {required_staff}")

            # Ensure Minimum Staffing Only for Essential Roles (Servers, Chefs, Managers)
            essential_roles = {
                "Server": 1,
                "Chef": 2,
                "Manager": 1
            }

            for role, min_required in essential_roles.items():
                required_staff[role] = max(required_staff.get(role, 0), min_required * 2)  # Ensure AM & PM coverage

            print(f"Adjusted Staffing Needs (Minimum Enforced for Essential Roles): {required_staff}")

            for role, count_needed in required_staff.items():
                # Debugging: Show All Employees for this Role
                all_role_employees = [emp.name for emp in employees if emp.role == role]
                print(f"All {role}s: {all_role_employees}")

                # Check if Employee is Available on This Day
                available_employees = [
                    emp for emp in employees if emp.role == role and any(str(day) in emp.availability for day in range(7))
                ]

                print(f"DEBUG: {role} Before Holiday Filtering: {[emp.name for emp in available_employees]}")

                # Exclude employees on approved holiday
                available_employees = [
                    emp for emp in available_employees if not HolidayRequest.query.filter_by(
                        employee_id=emp.id, date=current_date, status="Approved"
                    ).first()
                ]

                print(f"Available {role}s After Filtering: {[emp.name for emp in available_employees]}")

                # If No Employees Available, Skip Role (If Not Essential)
                if not available_employees:
                    print(f"No {role} available for {current_date}. Skipping role if not essential...")
                    if role in essential_roles:
                        print(f"ERROR: No essential role {role} available! Cannot generate schedule.")
                        return {"error": f"Not enough {role}s available to cover required shifts."}, 500
                    continue  # Skip optional roles if no employees are available

                assigned_employees = []

                # Ensure AM and PM shifts have minimum staff for essential roles
                am_shifts = max(essential_roles.get(role, 0), count_needed // 2) if role in essential_roles else count_needed // 2
                pm_shifts = count_needed - am_shifts

                # Adjust if not enough employees exist
                if len(available_employees) < count_needed:
                    am_shifts = min(len(available_employees) // 2, essential_roles.get(role, 0))
                    pm_shifts = len(available_employees) - am_shifts

                # Assign AM shifts
                for _ in range(am_shifts):
                    if available_employees:
                        employee = available_employees.pop(0)
                        assigned_employees.append((employee.id, "AM"))

                # Assign PM shifts
                for _ in range(pm_shifts):
                    if available_employees:
                        employee = available_employees.pop(0)
                        assigned_employees.append((employee.id, "PM"))

                print(f"Assigned {role}s: {assigned_employees}")

                for employee_id, shift_type in assigned_employees:
                    start_time = "10:00" if shift_type == "AM" else "17:00"
                    end_time = "17:00" if shift_type == "AM" else "23:00"

                    new_shift = Shift(
                        date=current_date,
                        shift_type=shift_type,
                        start_time=datetime.strptime(start_time, "%H:%M").time(),
                        end_time=datetime.strptime(end_time, "%H:%M").time(),
                        employee_id=employee_id,
                        role=role
                    )
                    db.session.add(new_shift)
                    print(f"Shift Created: {new_shift}")

            current_date += timedelta(days=1)

        print("Committing shifts to database...")
        db.session.commit()
        print("All shifts saved successfully!")

        return {"message": "Schedule generated successfully"}, 201
    except Exception as e:
        print(f"ERROR: {str(e)}")
        db.session.rollback()
        return {"error": str(e)}, 500




# API Endpoints

from flask_cors import cross_origin

@app.route('/')
def home():
    return "Welcome to the Employee Scheduling API! Visit /employees or /schedule"

@app.route('/employees', methods=['POST', 'GET'])
@cross_origin()  # Allow CORS for this route
def employees():
    if request.method == 'POST':
        data = request.json
        new_employee = Employee(
            name=data['name'],
            role=data['role'],
            availability=data.get('availability', ''),
            preferred_hours=data.get('preferred_hours', 40)
        )
        db.session.add(new_employee)
        db.session.commit()
        return jsonify({'message': 'Employee added successfully', 'id': new_employee.id}), 201

    elif request.method == 'GET':
        employees = Employee.query.all()
        return jsonify([
            {"id": emp.id, "name": emp.name, "role": emp.role, "availability": emp.availability}
            for emp in employees
        ]), 200
    
@app.route('/forecast', methods=['POST'])
def submit_forecast():
    data = request.json
    if not data or 'date' not in data or 'revenue' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        new_forecast = Forecast(
            date=datetime.strptime(data['date'], "%Y-%m-%d").date(),
            revenue=int(data['revenue'])
        )
        db.session.add(new_forecast)
        db.session.commit()
        return jsonify({'message': 'Forecast added successfully', 'id': new_forecast.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# GET method for fetching forecasts
@app.route('/forecast', methods=['GET'])
def get_forecasts():
    forecasts = Forecast.query.all()
    return jsonify([
        {"id": f.id, "date": f.date.strftime("%Y-%m-%d"), "revenue": f.revenue} for f in forecasts
    ]), 200


# DELETE an Employee
@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404

    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted successfully'}), 200

# UPDATE an Employee
@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404

    data = request.json
    employee.name = data.get('name', employee.name)
    employee.role = data.get('role', employee.role)
    employee.availability = data.get('availability', employee.availability)
    employee.preferred_hours = data.get('preferred_hours', employee.preferred_hours)

    db.session.commit()
    return jsonify({'message': 'Employee updated successfully'}), 200

@app.route('/forecast/<int:forecast_id>', methods=['DELETE'])
def delete_forecast(forecast_id):
    print(f"Delete request received for ID: {forecast_id}")  # Debugging

    forecast = Forecast.query.get(forecast_id)
    if not forecast:
        print("Forecast not found!")
        return jsonify({'error': 'Forecast not found'}), 404

    db.session.delete(forecast)
    db.session.commit()
    print(f"Forecast {forecast_id} deleted successfully!")
    
    return jsonify({'message': 'Forecast deleted successfully'}), 200


# UPDATE a Forecast
@app.route('/forecast/<int:forecast_id>', methods=['PUT'])
def update_forecast(forecast_id):
    forecast = Forecast.query.get(forecast_id)
    if not forecast:
        return jsonify({'error': 'Forecast not found'}), 404

    data = request.json
    forecast.date = datetime.strptime(data.get('date', forecast.date.strftime("%Y-%m-%d")), "%Y-%m-%d").date()
    forecast.revenue = data.get('revenue', forecast.revenue)

    db.session.commit()
    return jsonify({'message': 'Forecast updated successfully'}), 200

@app.route('/generate_schedule', methods=['POST'])
def generate_schedule_route():
    data = request.json
    if not data or 'start_date' not in data or 'end_date' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    return generate_schedule(data['start_date'], data['end_date'])

@app.route('/schedule', methods=['GET'])
def get_schedule():
    shifts = Shift.query.all()
    return jsonify([
        {"id": s.id, "date": s.date.strftime("%Y-%m-%d"), "shift_type": s.shift_type, 
         "start_time": s.start_time.strftime("%H:%M"), "end_time": s.end_time.strftime("%H:%M"),
         "employee_id": s.employee_id, "role": s.role}
        for s in shifts
    ]), 200

@app.route('/schedule/<date>', methods=['GET'])
def get_schedule_by_date(date):
    try:
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
        shifts = Shift.query.filter_by(date=selected_date).all()

        return jsonify([
            {
                "id": shift.id,
                "date": shift.date.strftime("%Y-%m-%d"),
                "shift_type": shift.shift_type,
                "start_time": shift.start_time.strftime("%H:%M"),
                "end_time": shift.end_time.strftime("%H:%M"),
                "employee_id": shift.employee_id,
                "role": shift.role
            }
            for shift in shifts
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/schedule/<date>', methods=['DELETE'])
def delete_schedule_by_date(date):
    try:
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
        deleted = Shift.query.filter_by(date=selected_date).delete()
        db.session.commit()

        if deleted:
            print(f"Deleted all shifts for {selected_date}")
            return jsonify({"message": f"Deleted schedule for {selected_date}"}), 200
        else:
            return jsonify({"message": "No shifts found for this date"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/holiday_requests', methods=['POST', 'GET'])
def handle_holiday_requests():
    if request.method == 'POST':
        data = request.json
        new_request = HolidayRequest(
            employee_id=data['employee_id'],
            date=datetime.strptime(data['date'], "%Y-%m-%d").date(),
            status="Pending"
        )
        db.session.add(new_request)
        db.session.commit()
        return jsonify({'message': 'Holiday request submitted successfully', 'id': new_request.id}), 201

    elif request.method == 'GET':
        requests = HolidayRequest.query.all()
        return jsonify([
            {
                "id": r.id,
                "employee_id": r.employee_id,
                "date": r.date.strftime("%Y-%m-%d"),
                "status": r.status
            }
            for r in requests
        ]), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

