from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'scheduler.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

db = SQLAlchemy(app)
jwt = JWTManager(app)

# === MODELS ===

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    availability = db.Column(db.Text, nullable=False)
    preferred_hours = db.Column(db.Integer, nullable=False)

class Forecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date, nullable=False)
    revenue = db.Column(db.Integer, nullable=False)

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date, nullable=False)
    shift_type = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    role = db.Column(db.String(50), nullable=False)

class HolidayRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="Pending")

with app.app_context():
    db.create_all()

# === AUTH ===

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({"token": token, "user_id": user.id}), 200
    return jsonify({"error": "Invalid username or password"}), 401

# === HELPERS ===

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

# === CRUD ROUTES ===

@app.route('/employees', methods=['POST', 'GET'])
@jwt_required()
def employees():
    user_id = get_jwt_identity()
    if request.method == 'POST':
        data = request.json
        emp = Employee(user_id=user_id, name=data['name'], role=data['role'],
                       availability=data.get('availability', ''), preferred_hours=data.get('preferred_hours', 40))
        db.session.add(emp)
        db.session.commit()
        return jsonify({"message": "Employee added", "id": emp.id}), 201
    employees = Employee.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": e.id, "name": e.name, "role": e.role, "availability": e.availability} for e in employees]), 200

@app.route('/employees/<int:employee_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def modify_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    if request.method == 'PUT':
        data = request.json
        employee.name = data.get('name', employee.name)
        employee.role = data.get('role', employee.role)
        employee.availability = data.get('availability', employee.availability)
        employee.preferred_hours = data.get('preferred_hours', employee.preferred_hours)
        db.session.commit()
        return jsonify({"message": "Employee updated"}), 200
    db.session.delete(employee)
    db.session.commit()
    return jsonify({"message": "Employee deleted"}), 200

@app.route('/forecast', methods=['POST', 'GET'])
@jwt_required()
def forecast():
    user_id = get_jwt_identity()
    if request.method == 'POST':
        data = request.json
        f = Forecast(user_id=user_id, date=datetime.strptime(data['date'], "%Y-%m-%d").date(), revenue=data['revenue'])
        db.session.add(f)
        db.session.commit()
        return jsonify({"message": "Forecast added", "id": f.id}), 201
    forecasts = Forecast.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": f.id, "date": f.date.strftime("%Y-%m-%d"), "revenue": f.revenue} for f in forecasts]), 200

@app.route('/forecast/<int:forecast_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def modify_forecast(forecast_id):
    forecast = Forecast.query.get_or_404(forecast_id)
    if request.method == 'PUT':
        data = request.json
        forecast.date = datetime.strptime(data['date'], "%Y-%m-%d").date()
        forecast.revenue = data['revenue']
        db.session.commit()
        return jsonify({"message": "Forecast updated"}), 200
    db.session.delete(forecast)
    db.session.commit()
    return jsonify({"message": "Forecast deleted"}), 200

@app.route('/holiday_requests', methods=['POST', 'GET'])
@jwt_required()
def holiday_requests():
    user_id = get_jwt_identity()
    if request.method == 'POST':
        data = request.json
        h = HolidayRequest(user_id=user_id, employee_id=data['employee_id'], date=datetime.strptime(data['date'], "%Y-%m-%d").date())
        db.session.add(h)
        db.session.commit()
        return jsonify({"message": "Request submitted", "id": h.id}), 201
    requests = HolidayRequest.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": r.id, "employee_id": r.employee_id, "date": r.date.strftime("%Y-%m-%d"), "status": r.status} for r in requests]), 200

@app.route('/holiday_requests/<int:request_id>', methods=['PUT'])
@jwt_required()
def update_holiday_request(request_id):
    req = HolidayRequest.query.get_or_404(request_id)
    req.status = request.json.get("status", req.status)
    db.session.commit()
    return jsonify({"message": "Request status updated"}), 200

@app.route('/generate_schedule', methods=['POST'])
@jwt_required()
def generate_schedule_route():
    user_id = get_jwt_identity()
    data = request.json
    start = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
    end = datetime.strptime(data['end_date'], "%Y-%m-%d").date()
    employees = Employee.query.filter_by(user_id=user_id).all()

    for single_date in (start + timedelta(n) for n in range((end - start).days + 1)):
        forecast = Forecast.query.filter_by(user_id=user_id, date=single_date).first()
        if not forecast:
            continue
        Shift.query.filter_by(user_id=user_id, date=single_date).delete()
        for role, count in get_required_staff(forecast.revenue).items():
            available = [e for e in employees if e.role == role]
            for i in range(min(len(available), count)):
                shift = Shift(user_id=user_id, date=single_date, shift_type="AM" if i < count // 2 else "PM",
                              start_time=datetime.strptime("10:00", "%H:%M").time() if i < count // 2 else datetime.strptime("17:00", "%H:%M").time(),
                              end_time=datetime.strptime("17:00", "%H:%M").time() if i < count // 2 else datetime.strptime("23:00", "%H:%M").time(),
                              employee_id=available[i].id, role=role)
                db.session.add(shift)
    db.session.commit()
    return jsonify({"message": "Schedule created"}), 201

@app.route('/schedule', methods=['GET'])
@jwt_required()
def get_schedule():
    user_id = get_jwt_identity()
    shifts = Shift.query.filter_by(user_id=user_id).all()
    return jsonify([
        {"id": s.id, "date": s.date.strftime("%Y-%m-%d"), "shift_type": s.shift_type,
         "start_time": s.start_time.strftime("%H:%M"), "end_time": s.end_time.strftime("%H:%M"),
         "employee_id": s.employee_id, "role": s.role}
        for s in shifts
    ]), 200

@app.route('/schedule/<date>', methods=['DELETE'])
@jwt_required()
def delete_schedule_by_date(date):
    user_id = get_jwt_identity()
    target_date = datetime.strptime(date, "%Y-%m-%d").date()
    Shift.query.filter_by(user_id=user_id, date=target_date).delete()
    db.session.commit()
    return jsonify({"message": f"Schedule deleted for {target_date}"}), 200

@app.route('/')
def home():
    return "✅ Employee Scheduling API is running."

if __name__ == "__main__":
    app.run(debug=True)
