from flask import Flask, render_template
from models import db, Employee
from utils import load_data, generate_visualizations

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def setup():
    db.create_all()  # Create database schema
    load_data()  # Load data from CSV

@app.route('/')
def dashboard():
    employees = Employee.query.all()
    generate_visualizations()
    return render_template('dashboard.html', employees=employees)

if __name__ == '__main__':
    app.run(debug=True)
