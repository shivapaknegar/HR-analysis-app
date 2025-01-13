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
        dataframe = pd.read_csv(filepath)
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
    average_income = dataframe['MonthlyIncome'].mean()
    largest_department = dataframe['Department'].value_counts().idxmax()
    largest_role = dataframe['JobRole'].value_counts().idxmax()

    data_summary = {
        'total_rows': dataframe.shape[0],
        'total_columns': dataframe.shape[1],
        'null_values': null_values
    }
    insights = {
        'average_income': f"${average_income:.2f}",
        'largest_department': largest_department,
        'largest_role': largest_role
    }

    return render_template('analysis.html', data_summary=data_summary, data_quality_score=data_quality_score, insights=insights)

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

    else:
        flash('Invalid graph type.')
        return redirect(url_for('analysis'))

if __name__ == '__main__':
    app.run(debug=True)
