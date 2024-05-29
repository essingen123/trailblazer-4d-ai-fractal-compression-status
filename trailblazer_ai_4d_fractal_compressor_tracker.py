import os
import sqlite3
import subprocess as sp
from flask import Flask, render_template, send_file
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

# Install necessary dependencies
def install_dependencies():
    try:
        sp.run('pip install Flask matplotlib numpy', shell=True, check=True)
    except sp.CalledProcessError as e:
        print(f"Dependency installation failed: {e}")
        raise

# Setup SQLite database
def setup_database():
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect('data/data.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sample (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        value INTEGER NOT NULL
    )
    ''')
    cursor.execute('INSERT INTO sample (name, value) VALUES (?, ?)', ('Sample1', 100))
    cursor.execute('INSERT INTO sample (name, value) VALUES (?, ?)', ('Sample2', 200))
    conn.commit()
    conn.close()

# Generate fractal image
def generate_fractal(filepath):
    x, y = np.meshgrid(np.linspace(-2, 2, 1000), np.linspace(-2, 2, 1000))
    c = x + 1j * y
    z = np.zeros_like(c)

    for _ in range(100):
        z = z**2 + c

    plt.figure(figsize=(8, 8))
    plt.imshow(np.abs(z), cmap='twilight_shifted', extent=(-2, 2, -2, 2))
    plt.axis('off')
    plt.title("Mandelbrot Set")
    plt.savefig(filepath, bbox_inches='tight', pad_inches=0)
    plt.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-fractal')
def fractal():
    generate_fractal('static/fractal.png')
    return send_file('static/fractal.png', mimetype='image/png')

@app.route('/data')
def get_data():
    conn = sqlite3.connect('data/data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sample')
    data = cursor.fetchall()
    conn.close()
    return {'data': data}

if __name__ == '__main__':
    # Install dependencies
    install_dependencies()

    # Setup database and directories
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    setup_database()

    # HTML template
    with open('templates/index.html', 'w') as f:
        f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trailblazer AI 4D Fractal Compressor Tracker</title>
</head>
<body>
    <h1>Trailblazer AI 4D Fractal Compressor Tracker</h1>
    <img src="/generate-fractal" alt="Fractal Image">
    <h2>Data</h2>
    <ul id="data-list"></ul>

    <script>
        fetch('/data')
            .then(response => response.json())
            .then(data => {
                const dataList = document.getElementById('data-list');
                data.data.forEach(item => {
                    const li = document.createElement('li');
                    li.textContent = `${item[1]}: ${item[2]}`;
                    dataList.appendChild(li);
                });
            });
    </script>
</body>
</html>
''')

    # Initialize Git repository
    try:
        sp.run('git init', shell=True, check=True)
        sp.run('git add .', shell=True, check=True)
        sp.run('git commit -m "Initial commit"', shell=True, check=True)
        sp.run('git remote add origin https://github.com/essingen123/python-to-ts-cyber-owl-tadpoles.git', shell=True, check=True)
        sp.run('git push -u origin master', shell=True, check=True)
    except sp.CalledProcessError as e:
        print(f"Git operation failed: {e}")

    # Run Flask app
    sp.Popen(['xdg-open', 'http://localhost:5000'])
    app.run(debug=True)
