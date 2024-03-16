from http.server import HTTPServer, BaseHTTPRequestHandler
import mysql.connector
import hashlib
from urllib.parse import parse_qs

# Load sensitive data from configuration file
from config import DB_CONFIG

# Connect to the MariaDB database
conn = mysql.connector.connect(**DB_CONFIG)

# Hash function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/register':
            # Serve registration form
            # Implement code to serve register.html template
        elif self.path == '/login':
            # Serve login form
            # Implement code to serve login.html template
        elif self.path.startswith('/user/dashboard'):
            # Serve user dashboard
            # Implement code to serve user_dashboard.html template
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        if self.path == '/register':
            # Process registration form submission
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)

            username = params['username'][0]
            password = params['password'][0]

            # Hash the password before storing
            hashed_password = hash_password(password)

            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
                conn.commit()
                # Redirect to login page after successful registration
                self.send_response(302)
                self.send_header('Location', '/login')
                self.end_headers()
            except mysql.connector.Error as err:
                print("Error:", err)
                self.send_response(500)
                self.end_headers()
            finally:
                cursor.close()
        elif self.path == '/login':
            # Process login form submission
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)

            username = params['username'][0]
            password = params['password'][0]

            # Hash the password before comparing
            hashed_password = hash_password(password)

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, hashed_password))
            user = cursor.fetchone()
            if user:
                if user[3] == 'admin':
                    # Redirect to admin dashboard
                    self.send_response(302)
                    self.send_header('Location', '/admin/dashboard')
                    self.end_headers()
                else:
                    # Redirect to user dashboard
                    self.send_response(302)
                    self.send_header('Location', '/user/dashboard')
                    self.end_headers()
            else:
                # Authentication failed
                self.send_response(302)
                self.send_header('Location', '/login')
                self.end_headers()
            cursor.close()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print('Server running...')
    httpd.serve_forever()
