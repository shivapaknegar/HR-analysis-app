import matplotlib.pyplot as plt
from models import Employee

def generate_visualizations():
    """
    Generate a simple bar chart showing employee distribution by years at the company.
    The chart will be saved in the static folder for use in the frontend.
    """
    # Query all employees from the database
    employees = Employee.query.all()

    # Create a dictionary to store the distribution of employees by years at the company
    distribution = {}
    for employee in employees:
        years = employee.years_at_company
        if years not in distribution:
            distribution[years] = 0
        distribution[years] += 1

    # Prepare data for the bar chart
    years = list(distribution.keys())
    counts = list(distribution.values())

    # Generate the bar chart
    plt.bar(years, counts)
    plt.xlabel('Years at Company')
    plt.ylabel('Number of Employees')
    plt.title('Employee Distribution by Years at Company')

    # Save the chart in the static folder
    plt.savefig('static/years_distribution.png')
    plt.close()
