from flask import Flask, render_template, request, redirect, flash
import sqlite3
from datetime import datetime  # Import datetime module to get the current date and time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for flash messages

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = '1234'

# Database initialization function
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        mobile TEXT NOT NULL,
        address TEXT NOT NULL,
        submission_time TEXT NOT NULL  -- New column for storing submission time
    )
    ''')
    conn.commit()
    conn.close()

# Route to show the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission and store data
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    mobile = request.form['mobile']
    address = request.form['address']
    submission_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get the current date and time
    
    # Insert into the database
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, mobile, address, submission_time) VALUES (?, ?, ?, ?)", 
              (name, mobile, address, submission_time))
    conn.commit()
    conn.close()
    
    return redirect('/')

# Route to display data in the database with login prompt
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if credentials are correct
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute("SELECT * FROM users")
            users = c.fetchall()
            conn.close()
            
            return render_template('admin.html', users=users)
        else:
            flash('Invalid username or password!')
            return redirect('/admin')
    
    # Display login form if GET request
    return render_template('login.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
