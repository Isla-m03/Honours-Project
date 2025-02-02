from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Workplace Scheduler API!"


# Database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, '../database/scheduler.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Employee model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    availability = db.Column(db.Text, nullable=False)
    preferred_hours = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Employee {self.name}>"

# Holiday Request model
class HolidayRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="Pending")  # Status: "Pending", "Approved", "Rejected"
    
    employee = db.relationship('Employee', backref=db.backref('holiday_requests', lazy=True))

    def __repr__(self):
        return f"<HolidayRequest Employee {self.employee_id} on {self.date} - {self.status}>"

# Create tables
with app.app_context():
    db.create_all()

# Routes
# 1. Submit a holiday request
@app.route('/holiday_requests', methods=['POST'])
def request_holiday():
    data = request.json
    try:
        employee_id = data['employee_id']
        date = datetime.strptime(data['date'], "%Y-%m-%d").date()

        # Check if employee exists
        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404

        new_request = HolidayRequest(employee_id=employee_id, date=date)
        db.session.add(new_request)
        db.session.commit()
        return jsonify({'message': 'Holiday request submitted successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 2. Get all holiday requests
@app.route('/holiday_requests', methods=['GET'])
def get_holiday_requests():
    requests = HolidayRequest.query.all()
    request_list = [
        {'id': r.id, 'employee_id': r.employee_id, 'date': r.date.strftime("%Y-%m-%d"), 'status': r.status}
        for r in requests
    ]
    return jsonify(request_list), 200

# 3. Approve/Reject a holiday request
@app.route('/holiday_requests/<int:id>', methods=['PUT'])
def update_holiday_request(id):
    data = request.json
    holiday_request = HolidayRequest.query.get_or_404(id)

    # Only allow status to be changed to "Approved" or "Rejected"
    if data.get('status') not in ["Approved", "Rejected"]:
        return jsonify({'error': 'Invalid status'}), 400

    holiday_request.status = data['status']
    db.session.commit()
    return jsonify({'message': f'Holiday request {id} {data["status"]}'}), 200

# 4. Get all holiday requests for a specific employee
@app.route('/employees/<int:employee_id>/holiday_requests', methods=['GET'])
def get_employee_holiday_requests(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    requests = HolidayRequest.query.filter_by(employee_id=employee_id).all()
    request_list = [
        {'id': r.id, 'date': r.date.strftime("%Y-%m-%d"), 'status': r.status}
        for r in requests
    ]
    return jsonify(request_list), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)