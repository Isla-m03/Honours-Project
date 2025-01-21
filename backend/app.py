from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)

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

# Create tables
with app.app_context():
    db.create_all()

# Routes
# 1. Add a new employee
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json
    try:
        new_employee = Employee(
            name=data['name'],
            role=data['role'],
            availability=data['availability'],
            preferred_hours=data['preferred_hours']
        )
        db.session.add(new_employee)
        db.session.commit()
        return jsonify({'message': 'Employee added successfully', 'employee': data}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 2. Get all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    employee_list = [
        {
            'id': emp.id,
            'name': emp.name,
            'role': emp.role,
            'availability': emp.availability,
            'preferred_hours': emp.preferred_hours
        }
        for emp in employees
    ]
    return jsonify(employee_list), 200

# 3. Get a single employee by ID
@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get_or_404(id)
    return jsonify({
        'id': employee.id,
        'name': employee.name,
        'role': employee.role,
        'availability': employee.availability,
        'preferred_hours': employee.preferred_hours
    }), 200

# 4. Update an employee by ID
@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.json
    employee = Employee.query.get_or_404(id)
    try:
        employee.name = data.get('name', employee.name)
        employee.role = data.get('role', employee.role)
        employee.availability = data.get('availability', employee.availability)
        employee.preferred_hours = data.get('preferred_hours', employee.preferred_hours)
        db.session.commit()
        return jsonify({'message': 'Employee updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 5. Delete an employee by ID
@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    try:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
