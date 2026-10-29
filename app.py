import os
from flask import Flask, render_template_string, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Environment variables se database details lena
DB_HOST = os.environ.get('DB_HOST', 'sdpi-mysql')
DB_PORT = int(os.environ.get('DB_PORT', 3306))
DB_NAME = os.environ.get('DB_NAME', 'sdpi_dashboard')
DB_USER = os.environ.get('DB_USER', 'sdpi_appuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '9VFMPiu45cEQducHqYNySNvNeIQBvEmHI-z73x6ml6qs_FmP')

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Database mein automatically test table banana
def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_entries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database connected and test table initialized!")
    except Exception as e:
        print(f"Database connection error: {e}")

# App start hote hi table initialize karein
init_db()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SDPI Dashboard - DB Connection Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f6f9; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); max-width: 500px; margin: 0 auto; }
        h2 { color: #2c3e50; }
        .status-success { color: green; font-weight: bold; }
        input[type="text"] { width: 70%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 8px 15px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        ul { list-style-type: none; padding: 0; }
        li { background: #e9ecef; margin: 5px 0; padding: 10px; border-radius: 4px; display: flex; justify-content: space-between; }
        .time { font-size: 0.8em; color: #6c757d; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Flask + MySQL Connection Test</h2>
        <p>Status: <span class="status-success">Connected to DB ({{ db_name }})</span></p>
        
        <form action="/add" method="POST">
            <input type="text" name="message" placeholder="Type a test entry..." required>
            <button type="submit">Add Entry</button>
        </form>

        <h3>Entries Saved in MySQL:</h3>
        <ul>
            {% for entry in entries %}
                <li>
                    <span>{{ entry[1] }}</span>
                    <span class="time">{{ entry[2] }}</span>
                </li>
            {% else %}
                <li>No entries yet. Add one above!</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, message, created_at FROM test_entries ORDER BY id DESC")
        entries = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template_string(HTML_TEMPLATE, entries=entries, db_name=DB_NAME)
    except Exception as e:
        return f"<h3>Database Connection Error:</h3> <p>{e}</p>"

@app.route('/add', methods=['POST'])
def add():
    message = request.form.get('message')
    if message:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO test_entries (message) VALUES (%s)", (message,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)