"""
# Main Flask application file that:
- Handles routing (URLs like '/', '/projects', '/about', etc.)
- Defines what content to show on each page
- Contains project data (in the projects list)
- Manages server-side logic

Usage: 
Whenever you add a new project or new page, you likely will (1) need to add a new route in the 
app.py file AND (2) add a new template file in the templates folder. Moreover, this is the file 
where you will add the python code (function) to execute in the visualization for each 
project page. The python code should be in a separate file in separate folder, 
such as in the project1_python_files folder.
"""

import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-GUI rendering

import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template, jsonify
from project1_python_files.sample_visualization import sample_visualization
from project1_python_files.network_cases_visualization import load_data
from project1_python_files.network_cases_visualization import create_flu_figure

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/project1')
def project1():
    return create_flu_figure()

@app.route('/project2')
def project2():
    return render_template('project2.html')

@app.route('/update_plot/<date>')
def update_plot(date):
    return create_flu_figure(selected_date=date)

if __name__ == '__main__':
    app.run(debug=True)