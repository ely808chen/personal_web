"""
# Main Flask application file that:
- Handles routing (URLs like '/', '/projects', '/about', etc.)
- Defines what content to show on each page
- Contains project data (in the projects list)
- Manages server-side logic
"""


from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', year=datetime.now().year)

@app.route('/projects')
def projects():
    projects = [
        {
            'title': 'Project 1',
            'description': 'Description of project 1',
            'technologies': ['Python', 'TensorFlow', 'Flask'],
            'github_link': '#'
        }
    ]
    return render_template('projects.html', projects=projects, year=datetime.now().year)

@app.route('/about')
def about():
    return render_template('about.html', year=datetime.now().year)

@app.route('/contact')
def contact():
    return render_template('contact.html', year=datetime.now().year)

if __name__ == '__main__':
    app.run(debug=True, port=5001) 