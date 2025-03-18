import sqlite3
from admin_dashboard import admin_menu
from user_dashboard import user_menu

# Function to create a connection to the SQLite database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('library.db')  # Connect to the database
        print("Connection to SQLite DB successful!")
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite DB: {e}")
    return conn

# Function to authenticate a user
def login(username, password):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()

            # Trim whitespace from inputs
            username = username.strip()
            password = password.strip()

            # Debug: Print the query and inputs
            print(f"Executing query: SELECT * FROM Users WHERE username = '{username}' AND password = '{password}'")

            # Check if the username and password match
            cursor.execute('''
                SELECT * FROM Users WHERE username = ? AND password = ?
            ''', (username, password))

            user = cursor.fetchone()  # Fetch the user record

            # Debug: Print the fetched user
            print(f"Fetched user: {user}")

            if user:
                print(f"Login successful! Welcome, {user[1]}.")
                return user  # Return the user record
            else:
                print("Invalid username or password.")
                return None

        except sqlite3.Error as e:
            print(f"Error during login: {e}")
        finally:
            conn.close()  # Close the connection

# Function to display the login menu
def login_menu():
    print("\n--- Library Management System Login ---")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    user = login(username, password)
    if user:
        if user[3] == "admin":  # Check the user's role
            admin_menu()  # Redirect to admin dashboard
        else:
            user_menu(user[0])  # Redirect to user dashboard with user ID
    else:
        print("Login failed. Please try again.")

# Main function to test the login system
if __name__ == "__main__":
    login_menu()