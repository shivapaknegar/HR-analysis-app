import pandas as pd
from models import db, Employee

def load_data():
    # Load data from the provided CSV file
    data = pd.read_csv('data/H-R-IBM.csv')
    
    # Rename columns to match the database schema
    data.rename(columns={
        'Department': 'department',
        'JobRole': 'role',
        'Gender': 'gender',
        'YearsAtCompany': 'years_at_company',
        'Attrition': 'attrition'  # Assuming 'Attrition' is included in your CSV
    }, inplace=True)

    # Add each row to the database
    for _, row in data.iterrows():
        employee = Employee(
            department=row['department'],
            role=row['role'],
            gender=row['gender'],
            years_at_company=row['years_at_company'],
            attrition=row.get('attrition', None)  # Handle optional 'Attrition' column
        )
        db.session.add(employee)
    db.session.commit()
