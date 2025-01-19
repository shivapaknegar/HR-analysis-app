# HR Analysis App

## Overview
The HR Analysis App is designed to simplify HR data analysis by enabling users to upload datasets, validate data quality, and generate insightful visualizations. Developed as a part of a simulated consultancy project, this application serves HR departments with limited technical expertise by automating complex data analysis tasks.

---

## Features

### 1. File Upload
- Upload Excel files directly through the application.
- Validate file format and ensure all required columns are present.

### 2. Data Quality Assessment
- Identify null values and calculate a data quality score.
- Provide an overview of dataset completeness.

### 3. Insights and Metrics
- Attrition rate analysis by department, role, and gender.
- Workforce distribution by department, role, and years at the company.
- Monthly income trends and job satisfaction insights.

### 4. Visualizations
- Bar charts for gender and department distributions.
- Pie charts for attrition rates.
- Histograms for income and age distributions.

### 5. Responsive Dashboard
- Modern and intuitive UI for displaying key metrics and insights.
- Designed to be accessible on all devices.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/shivapaknegar/hr-analysis-app.git
   cd hr-analysis-app
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   flask --app app.py run --debug
   ```

5. **Access the App**
   - Open your web browser and navigate to: `http://127.0.0.1:5000`

---

## Usage

### Steps to Use the App

1. **Upload Data**
   - Go to the homepage.
   - Upload an Excel file containing HR data. Ensure the file has 35 columns and follows the required format.

2. **Analyze Data**
   - Once uploaded, the app validates the dataset.
   - Navigate to the dashboard to view:
     - Key metrics like total rows, columns, and null values.
     - Attrition analysis and other visual insights.

3. **Generate Graphs**
   - Use the provided options to generate specific visualizations, such as:
     - Attrition rates by department.
     - Gender distribution.
     - Income distribution.

4. **Export Insights**
   - Export summaries or screenshots of visualizations for reporting purposes.

---

## Project Structure

```
HR-analysis-app/
├── app.py                 # Main Flask application
├── templates/             # HTML templates
│   ├── index.html         # Homepage template
│   ├── analysis.html      # Dashboard template
├── static/                # Static files (CSS, images, etc.)
│   ├── style.css          # CSS for styling the app
│   └── charts/            # Folder for generated charts
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── data/                  # Folder for uploaded datasets
```

---

## Technologies Used
- **Flask**: For building the web application.
- **Pandas**: For data processing and analysis.
- **Matplotlib**: For creating visualizations.
- **HTML/CSS**: For frontend design.

---

## Future Improvements
1. **Cloud Integration**
   - Host the app on AWS or Google Cloud to handle larger datasets and provide real-time analysis.

2. **Database Support**
   - Replace file-based uploads with a relational database like PostgreSQL for scalable storage.

3. **Advanced Analytics**
   - Incorporate machine learning models to predict attrition and identify key drivers.

4. **Multi-Tenant Support**
   - Allow multiple companies or departments to use the app simultaneously with secure data segregation.

5. **Enhanced User Management**
   - Add login functionality and role-based access controls for improved security.

---

## Contributors
- **Reza**: Project Manager
- **Shiva**: Lead Developer
- **Snezhana**: API Tester and Documentation Specialist
- **Danny**: UI Designer and Frontend Developer

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
