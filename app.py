from flask import Flask, request, render_template, redirect, url_for, flash
import pandas as pd
import matplotlib.pyplot as plt
import os

class Reading:

   def __init__(self, age, travel, daily_rate):
       self.Age = age 
       self.BusinessTravel = travel
       self.DailyRate = daily_rate
 
app = Flask(__name__)
app.secret_key = 'your_secret_key'
 
UPLOAD_FOLDER = 'data'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
# Global variable for the uploaded DataFrame
dataframe = None
filename = os.path.join(app.config['UPLOAD_FOLDER'], 'H-R-IBM.csv')
if os.path.exists:
    dataframe = pd.read_csv(filename)
 
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/upload', methods=['POST'])
def upload_file():
    global dataframe
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        dataframe = pd.read_csv(filepath)
        dataframe.to_json()
        flash('File uploaded successfully!')
        return redirect(url_for('analysis'))
 
@app.route('/api/departments')
def list_departments():
    global dataframe

    return dataframe['Department'].unique().tolist();

@app.route('/api/roles')
def list_roles():
    global dataframe

    return dataframe['JobRole'].unique().tolist();

def to_response(data):
    return list(map(lambda x:Reading(x[0],x[2],x[3]).__dict__,data.values.tolist()))

@app.route('/api/employees')
def filter_employees():
    global dataframe

    data=dataframe
    filter_department=request.args.get('department')
    filter_role=request.args.get('role')
    filter_gender=request.args.get('gender')
    filter_yoe=request.args.get('experience')
    if filter_department:
        data=data[data.Department==filter_department]
    if filter_role:
        data=data[data.JobRole==filter_role]
    if filter_gender:
        data=data[data.Gender==filter_gender]
    if filter_yoe:
        data=data[data.TotalWorkingYears > int(filter_yoe)]
    
    #return list(map(lambda x:Reading(x[0],x[2],x[3]).__dict__,data.values.tolist()))
    return to_response(data)

@app.route('/analysis')
def analysis():
    global dataframe
    if dataframe is None:
        flash('No data uploaded.')
        return redirect(url_for('index'))
    
    # Data quality check
    null_values = dataframe.isnull().sum().sum()
    data_summary = {
        'total_rows': dataframe.shape[0],
        'total_columns': dataframe.shape[1],
        'null_values': null_values
    }
    return render_template('analysis.html', data_summary=data_summary)
 
@app.route('/generate-graph/<graph_type>')
def generate_graph(graph_type):
    global dataframe
    if dataframe is None:
        flash('No data uploaded.')
        return redirect(url_for('index'))
    
    null_values = dataframe.isnull().sum().sum()
    data_summary = {
        'total_rows': dataframe.shape[0],
        'total_columns': dataframe.shape[1],
        'null_values': null_values
    }
 
    if graph_type == 'gender_distribution':
        gender_counts = dataframe['Gender'].value_counts()
        gender_counts.plot(kind='bar', color=['blue', 'pink'])
        plt.title('Gender Distribution')
        plt.xlabel('Gender')
        plt.ylabel('Count')
        plt.savefig('static/gender_distribution.png')
        plt.close()
        return render_template('analysis.html', graph='/static/gender_distribution.png', data_summary=data_summary)
 
    elif graph_type == 'average_income':
        avg_income = dataframe['MonthlyIncome'].mean()
        flash(f'Average Monthly Income: {avg_income}')
        return redirect(url_for('analysis'))
 
    elif graph_type == 'job_roles':
        job_counts = dataframe['JobRole'].value_counts()
        job_counts.plot(kind='bar', color='green')
        plt.title('Job Roles with Highest Count')
        plt.xlabel('Job Role')
        plt.ylabel('Count')
        plt.savefig('static/job_roles.png')
        plt.close()
        return render_template('analysis.html', graph='/static/job_roles.png', data_summary=data_summary)
 
    elif graph_type == 'department_count':
        department_counts = dataframe['Department'].value_counts()
        department_counts.plot(kind='bar', color='purple')
        plt.title('Employees per Department')
        plt.xlabel('Department')
        plt.ylabel('Count')
        plt.savefig('static/department_count.png')
        plt.close()
        return render_template('analysis.html', graph='/static/department_count.png', data_summary=data_summary)
 
    else:
        flash('Invalid graph type.')
        return redirect(url_for('index'))
 
if __name__ == '__main__':
    app.run(debug=True)