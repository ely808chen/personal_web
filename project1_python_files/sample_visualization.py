import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-GUI rendering

import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template

def sample_visualization():
    # Create a simple plot as an example
    plt.figure(figsize=(6, 4))
    plt.plot([1, 2, 3, 4], [10, 20, 25, 30], marker='o')
    plt.title('Project 1 Visualization')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')

    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data = base64.b64encode(buf.read()).decode('utf8')

    return render_template('project1.html', plot_data=plot_data)