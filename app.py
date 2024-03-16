from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
import os
import mysql.connector

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Set up session secret key
app.secret_key = os.urandom(24)

# Connect to the MariaDB database
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login form submission
        username = request.form['username']
        password = request.form['password']

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        if user and bcrypt.check_password_hash(user[2], password):
            session['username'] = username
            if user[3] == 'admin':
                # Redirect to admin dashboard
                return redirect(url_for('admin_dashboard'))
            else:
                # Redirect to user dashboard
                return redirect(url_for('user_dashboard'))
        else:
            # Authentication failed
            return render_template('login.html', error='Invalid username or password')

    # Render login page for GET request
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration form submission
        username = request.form['username']
        password = request.form['password']

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            # Redirect to login page after successful registration
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            # Handle database error
            return render_template('register.html', error='Error: {}'.format(err))

    # Render registration page for GET request
    return render_template('register.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'username' in session:
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/user/dashboard')
def user_dashboard():
    if 'username' in session:
        return render_template('user_dashboard.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
