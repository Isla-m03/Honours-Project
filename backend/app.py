from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime, timedelta

# Initialize Flask app
app = Flask(__name__)

# Database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'scheduler.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models

# Employee model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)  # e.g., Server, Chef, Bartender
    availability = db.Column(db.Text, nullable=False)  # e.g., "Mon-Fri 10:00-23:00"
    preferred_hours = db.Column(db.Integer, nullable=False)  # Weekly target hours

# Holiday Request model
class HolidayRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="Pending")
    employee = db.relationship('Employee', backref=db.backref('holiday_requests', lazy=True))

# Shift model
class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    shift_type = db.Column(db.String(50), nullable=False)  # AM or PM
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)  # Assigned employee
    role = db.Column(db.String(50), nullable=False)  # Role required (Server, Chef, etc.)

    employee = db.relationship('Employee', backref=db.backref('shifts', lazy=True))

# Forecast model
class Forecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    revenue = db.Column(db.Integer, nullable=False)  # Predicted revenue for the day

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Define required staff per revenue forecast
def get_required_staff(revenue):
    """Determines required staff based on forecasted revenue."""
    if revenue < 2000:
        return {"Server": 1, "Chef": 2}
    elif revenue < 5000:
        return {"Server": 3, "Chef": 3, "Bartender": 1}
    elif revenue < 8000:
        return {"Server": 7, "Chef": 5, "Bartender": 1, "Server Assistant": 1, "Door Host": 1}
    else:
        return {"Server": 10, "Chef": 7, "Bartender": 2, "Server Assistant": 2, "Door Host": 2}

# Generate schedule
def generate_schedule(start_date, end_date):
    """Automatically creates a rota based on forecasted demand."""
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        employees = Employee.query.all()

        current_date = start_date
        while current_date <= end_date:
            forecast = Forecast.query.filter_by(date=current_date).first()
            if not forecast:
                current_date += timedelta(days=1)
                continue  # Skip days without a forecast

            required_staff = get_required_staff(forecast.revenue)

            for role, count_needed in required_staff.items():
                available_employees = [
                    emp for emp in employees if emp.role == role and str(current_date.weekday()) in emp.availability
                ]

                # Exclude employees on approved holiday
                available_employees = [
                    emp for emp in available_employees if not HolidayRequest.query.filter_by(
                        employee_id=emp.id, date=current_date, status="Approved"
                    ).first()
                ]

                # Sort employees by those with fewer weekly hours worked
                available_employees.sort(key=lambda emp: sum(
                    (s.end_time.hour - s.start_time.hour) for s in emp.shifts if s.date >= current_date - timedelta(days=current_date.weekday())
                ))

                assigned_employees = []
                for _ in range(count_needed):
                    if available_employees:
                        employee = available_employees.pop(0)
                        assigned_employees.append(employee.id)
                        available_employees.append(employee)  # Rotate for fairness

                # Save shifts
                for employee_id in assigned_employees:
                    new_shift = Shift(
                        date=current_date,
                        shift_type="AM" if _ < count_needed // 2 else "PM",
                        start_time=datetime.strptime("10:00", "%H:%M").time(),
                        end_time=datetime.strptime("23:00", "%H:%M").time(),
                        employee_id=employee_id,
                        role=role
                    )
                    db.session.add(new_shift)

            current_date += timedelta(days=1)  # Move to next day

        db.session.commit()
        return {"message": "Schedule generated successfully"}, 201
    except Exception as e:
        return {"error": str(e)}, 500

# API Endpoints

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json
    if not data or 'name' not in data or 'role' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    new_employee = Employee(
        name=data['name'],
        role=data['role'],
        availability=data.get('availability', ''),
        preferred_hours=data.get('preferred_hours', 0)
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Employee added successfully', 'id': new_employee.id}), 201

@app.route('/forecast', methods=['POST'])
def submit_forecast():
    data = request.json
    if not data or 'date' not in data or 'revenue' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    new_forecast = Forecast(date=datetime.strptime(data['date'], "%Y-%m-%d").date(), revenue=data['revenue'])
    db.session.add(new_forecast)
    db.session.commit()
    return jsonify({'message': 'Forecast added successfully'}), 201

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

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
