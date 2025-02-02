from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

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
    role = db.Column(db.String(80), nullable=False)
    availability = db.Column(db.Text, nullable=False)
    preferred_hours = db.Column(db.Integer, nullable=False)

# Holiday Request model
class HolidayRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="Pending")
    employee = db.relationship('Employee', backref=db.backref('holiday_requests', lazy=True))

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Routes

# 1. Add an employee
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json
    try:
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 2. Get all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    employee_list = [{'id': e.id, 'name': e.name, 'role': e.role, 'availability': e.availability, 'preferred_hours': e.preferred_hours} for e in employees]
    return jsonify(employee_list), 200

# 3. Submit a holiday request
@app.route('/holiday_requests', methods=['POST'])
def request_holiday():
    data = request.json
    try:
        if not data or 'employee_id' not in data or 'date' not in data:
            return jsonify({'error': 'Missing required fields: employee_id, date'}), 400

        employee_id = data['employee_id']
        date_str = data['date']

        # Convert date
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        # Check if employee exists
        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404

        # Check for duplicate request on the same date
        existing_request = HolidayRequest.query.filter_by(employee_id=employee_id, date=date).first()
        if existing_request:
            return jsonify({'error': 'Holiday request already exists for this date'}), 400

        new_request = HolidayRequest(employee_id=employee_id, date=date)
        db.session.add(new_request)
        db.session.commit()
        return jsonify({'message': 'Holiday request submitted successfully', 'id': new_request.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 4. Get all holiday requests
@app.route('/holiday_requests', methods=['GET'])
def get_holiday_requests():
    requests = HolidayRequest.query.all()
    request_list = [{'id': r.id, 'employee_id': r.employee_id, 'date': r.date.strftime("%Y-%m-%d"), 'status': r.status} for r in requests]
    return jsonify(request_list), 200

# 5. Approve or reject a holiday request
@app.route('/holiday_requests/<int:id>', methods=['PUT'])
def update_holiday_request(id):
    data = request.json
    holiday_request = HolidayRequest.query.get_or_404(id)

    if 'status' not in data or data['status'] not in ['Approved', 'Rejected']:
        return jsonify({'error': 'Invalid status. Use "Approved" or "Rejected"'}), 400

    holiday_request.status = data['status']
    db.session.commit()
    return jsonify({'message': f'Holiday request {id} {data["status"]}'}), 200

# 6. Get holiday requests for a specific employee
@app.route('/employees/<int:employee_id>/holiday_requests', methods=['GET'])
def get_employee_holiday_requests(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    requests = HolidayRequest.query.filter_by(employee_id=employee_id).all()
    request_list = [{'id': r.id, 'date': r.date.strftime("%Y-%m-%d"), 'status': r.status} for r in requests]
    return jsonify(request_list), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
