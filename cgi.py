#!/usr/bin/env python

import cgitb
import cgi
import mysql.connector

# Enable CGI error reporting
cgitb.enable()

# Print the HTTP header
print("Content-Type: text/html\n")

# Connect to the MariaDB database
try:
    conn = mysql.connector.connect(
        host="rdbms.strato.de",
        user="dbu3805768",
        password="SQcWLEg5BAR5qVv",
        database="dbs12691858"
    )
except mysql.connector.Error as err:
    print("Database connection error:", err)

# Create a cursor object
cursor = conn.cursor()

# Process the form data
form = cgi.FieldStorage()
if "action" in form:
    action = form.getvalue("action")
    if action == "login":
        username = form.getvalue("username")
        password = form.getvalue("password")
        # Validate the login credentials
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if user:
            print("<h1>Login Successful</h1>")
        else:
            print("<h1>Login Failed</h1>")
    elif action == "register":
        username = form.getvalue("username")
        password = form.getvalue("password")
        # Insert new user into the database
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            print("<h1>Registration Successful</h1>")
        except mysql.connector.Error as err:
            print("<h1>Error: {}</h1>".format(err))
else:
    print("<h1>No action specified</h1>")

# Print the login and registration forms
print("<h2>Login</h2>")
print('<form action="/cgi-bin/your_cgi_script.py" method="post">')
print('<input type="hidden" name="action" value="login">')
print('Username: <input type="text" name="username"><br>')
print('Password: <input type="password" name="password"><br>')
print('<input type="submit" value="Login">')
print('</form>')

print("<h2>Register</h2>")
print('<form action="/cgi-bin/your_cgi_script.py" method="post">')
print('<input type="hidden" name="action" value="register">')
print('Username: <input type="text" name="username"><br>')
print('Password: <input type="password" name="password"><br>')
print('<input type="submit" value="Register">')
print('</form>')

# Close the database connection
cursor.close()
conn.close()
