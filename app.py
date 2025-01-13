from flask import Flask, request, render_template, redirect, url_for, flash
import pandas as pd
import os
import matplotlib.pyplot as plt

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure upload folder
UPLOAD_FOLDER = 'data'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global variable to store the uploaded DataFrame
dataframe = None

@app.route('/')
def index():
    """
    Render the homepage where users can upload the file.
    """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and save it to the server.
    """
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
        dataframe = pd.read_excel(filepath)
        flash('File uploaded successfully!')
        return redirect(url_for('analysis'))

@app.route('/analysis')
def analysis():
    """
    Analyze the uploaded dataset and display key metrics.
    """
    global dataframe
    if dataframe is None:
        flash('No data uploaded.')
        return redirect(url_for('index'))

    # Data quality checks
    null_values = dataframe.isnull().sum().sum()
    data_quality_score = round((1 - (null_values / (dataframe.shape[0] * dataframe.shape[1]))) * 100, 2)

    # Key insights
    attrition_by_department = dataframe.groupby('Department')['Attrition'].apply(lambda x: (x == 'Yes').mean() * 100).round(2).to_dict()
    insights = {
        'total_rows': dataframe.shape[0],
        'total_columns': dataframe.shape[1],
        'null_values': null_values,
        'data_quality_score': data_quality_score,
        'average_income': f"${dataframe['MonthlyIncome'].mean():.2f}",
        'largest_department': dataframe['Department'].value_counts().idxmax(),
        'largest_role': dataframe['JobRole'].value_counts().idxmax(),
        'attrition_rate': round((dataframe['Attrition'].value_counts(normalize=True).get('Yes', 0) * 100), 2),
        'highest_attrition_dept': max(attrition_by_department, key=attrition_by_department.get),
        'attrition_by_department': attrition_by_department
    }

    return render_template('analysis.html', data_summary={
        'total_rows': insights['total_rows'],
        'total_columns': insights['total_columns'],
        'null_values': insights['null_values'],
        'data_quality_score': insights['data_quality_score']
    }, insights=insights)

@app.route('/generate-graph/<graph_type>')
def generate_graph(graph_type):
    """
    Generate visualizations based on the uploaded dataset.
    """
    global dataframe
    if dataframe is None:
        flash('No data uploaded.')
        return redirect(url_for('index'))

    if graph_type == 'gender_distribution':
        gender_counts = dataframe['Gender'].value_counts()
        gender_counts.plot(kind='bar', color=['blue', 'pink'])
        plt.title('Gender Distribution')
        plt.xlabel('Gender')
        plt.ylabel('Count')
        plt.savefig('static/gender_distribution.png')
        plt.close()
        return render_template('analysis.html', graph='static/gender_distribution.png')

    elif graph_type == 'department_count':
        department_counts = dataframe['Department'].value_counts()
        department_counts.plot(kind='bar', color='purple')
        plt.title('Employees per Department')
        plt.xlabel('Department')
        plt.ylabel('Count')
        plt.savefig('static/department_count.png')
        plt.close()
        return render_template('analysis.html', graph='static/department_count.png')

    elif graph_type == 'attrition_rate':
        attrition_counts = dataframe['Attrition'].value_counts()
        attrition_counts.plot(kind='pie', autopct='%1.1f%%', colors=['green', 'red'])
        plt.title('Attrition Rate')
        plt.ylabel('')
        plt.savefig('static/attrition_rate.png')
        plt.close()
        return render_template('analysis.html', graph='static/attrition_rate.png')

    elif graph_type == 'income_distribution':
        dataframe['MonthlyIncome'].plot(kind='hist', bins=20, color='blue', alpha=0.7)
        plt.title('Monthly Income Distribution')
        plt.xlabel('Monthly Income')
        plt.ylabel('Frequency')
        plt.savefig('static/income_distribution.png')
        plt.close()
        return render_template('analysis.html', graph='static/income_distribution.png')

    else:
        flash('Invalid graph type.')
        return redirect(url_for('analysis'))

if __name__ == '__main__':
    app.run(debug=True)
