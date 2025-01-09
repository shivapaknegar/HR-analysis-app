from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    years_at_company = db.Column(db.Integer, nullable=False)
    attrition = db.Column(db.String(10), nullable=True)  # Include 'Attrition' field if applicable
