from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity
)
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///scheduler.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret"
db = SQLAlchemy(app)
jwt = JWTManager(app)

# ======================= MODELS ==========================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(80))
    role = db.Column(db.String(80))
    availability = db.Column(db.String(120))
    preferred_hours = db.Column(db.Integer)

class Forecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.Date)
    revenue = db.Column(db.Integer)

class HolidayRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"))
    date = db.Column(db.Date)
    status = db.Column(db.String(20), default="Pending")

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.Date)
    shift_type = db.Column(db.String(10))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"))
    role = db.Column(db.String(50))

with app.app_context():
    db.create_all()

# ======================= AUTH ==========================

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400
    user = User(
        username=data["username"],
        email=data["email"]
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()

    if user and user.check_password(data["password"]):
        # ✅ Convert user.id to string to meet JWT requirements
        token = create_access_token(identity=str(user.id))
        return jsonify({"token": token, "user_id": user.id}), 200

    return jsonify({"error": "Invalid credentials"}), 401

# ======================= EMPLOYEES ==========================

@app.route("/employees", methods=["GET", "POST"])
@jwt_required()
def employees():
    user_id = get_jwt_identity()

    if request.method == "POST":
        data = request.json
        new_emp = Employee(
            user_id=user_id,
            name=data["name"],
            role=data["role"],
            availability=data["availability"],
            preferred_hours=data["preferred_hours"]
        )
        db.session.add(new_emp)
        db.session.commit()
        return jsonify({"message": "Employee added"}), 201

    employees = Employee.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": e.id, "name": e.name, "role": e.role,
        "availability": e.availability, "preferred_hours": e.preferred_hours
    } for e in employees]), 200

@app.route("/employees/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_employee(id):
    user_id = get_jwt_identity()
    emp = Employee.query.filter_by(id=id, user_id=user_id).first()
    if not emp:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(emp)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200

# ======================= FORECAST ==========================

@app.route("/forecast", methods=["GET", "POST"])
@jwt_required()
def forecast():
    user_id = get_jwt_identity()

    if request.method == "POST":
        data = request.json
        new_forecast = Forecast(
            user_id=user_id,
            date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
            revenue=int(data["revenue"])
        )
        db.session.add(new_forecast)
        db.session.commit()
        return jsonify({"message": "Forecast added"}), 201

    forecasts = Forecast.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": f.id, "date": f.date.strftime("%Y-%m-%d"), "revenue": f.revenue
    } for f in forecasts]), 200

# ======================= HOLIDAY ==========================

@app.route("/holiday_requests", methods=["GET", "POST"])
@jwt_required()
def holiday_requests():
    user_id = get_jwt_identity()

    if request.method == "POST":
        data = request.json
        req = HolidayRequest(
            user_id=user_id,
            employee_id=data["employee_id"],
            date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
            status="Pending"
        )
        db.session.add(req)
        db.session.commit()
        return jsonify({"message": "Request submitted"}), 201

    requests = HolidayRequest.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": r.id, "employee_id": r.employee_id,
        "date": r.date.strftime("%Y-%m-%d"), "status": r.status
    } for r in requests]), 200

# ======================= SCHEDULE ==========================

@app.route("/generate_schedule", methods=["POST"])
@jwt_required()
def generate_schedule():
    user_id = get_jwt_identity()
    data = request.json
    start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
    end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()

    employees = Employee.query.filter_by(user_id=user_id).all()
    forecasts = {f.date: f.revenue for f in Forecast.query.filter_by(user_id=user_id).all()}

    current_date = start_date
    while current_date <= end_date:
        revenue = forecasts.get(current_date, 0)

        # logic example: adjust for revenue
        required_roles = {
            "Chef": 2 if revenue > 0 else 0,
            "Server": 2 if revenue > 0 else 0,
            "Manager": 1 if revenue > 0 else 0,
        }

        for role, count in required_roles.items():
            available = [e for e in employees if e.role == role]
            for i in range(count):
                if i < len(available):
                    shift = Shift(
                        user_id=user_id,
                        date=current_date,
                        shift_type="AM" if i % 2 == 0 else "PM",
                        start_time=datetime.strptime("10:00", "%H:%M").time() if i % 2 == 0 else datetime.strptime("17:00", "%H:%M").time(),
                        end_time=datetime.strptime("17:00", "%H:%M").time() if i % 2 == 0 else datetime.strptime("23:00", "%H:%M").time(),
                        employee_id=available[i].id,
                        role=role
                    )
                    db.session.add(shift)
        current_date += timedelta(days=1)

    db.session.commit()
    return jsonify({"message": "Schedule generated"}), 201

@app.route("/schedule", methods=["GET"])
@jwt_required()
def get_schedule():
    user_id = get_jwt_identity()
    shifts = Shift.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": s.id, "date": s.date.strftime("%Y-%m-%d"),
        "shift_type": s.shift_type,
        "start_time": s.start_time.strftime("%H:%M"),
        "end_time": s.end_time.strftime("%H:%M"),
        "employee_id": s.employee_id,
        "role": s.role
    } for s in shifts]), 200

# ======================= START ==========================

@app.route("/")
def home():
    return "API is live", 200

if __name__ == "__main__":
    app.run(debug=True)
