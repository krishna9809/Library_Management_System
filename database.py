import sqlite3

def insert_sample_data(conn):
    try:
        cursor = conn.cursor()

        # Insert an admin user
        cursor.execute('''
            INSERT INTO Users (username, password, role)
            VALUES (?, ?, ?)
        ''', ("admin", "admin123", "admin"))

        # Insert a normal user
        cursor.execute('''
            INSERT INTO Users (username, password, role)
            VALUES (?, ?, ?)
        ''', ("user1", "user123", "user"))

        # Insert some books
        cursor.execute('''
            INSERT INTO Books (title, author)
            VALUES (?, ?)
        ''', ("Python Programming", "John Doe"))

        cursor.execute('''
            INSERT INTO Books (title, author)
            VALUES (?, ?)
        ''', ("SQL for Beginners", "Jane Smith"))

        conn.commit()
        print("Sample data inserted successfully!")
    except sqlite3.Error as e:
        print(f"Error inserting sample data: {e}")


# Function to create a connection to the SQLite database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('library.db')  # Create or connect to the database
        print("Connection to SQLite DB successful!")
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite DB: {e}")
    return conn

# Function to create tables
def create_tables(conn):
    try:
        cursor = conn.cursor()

        # Create Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')

        # Create Books table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                available INTEGER DEFAULT 1  -- 1 for available, 0 for issued
            )
        ''')

        # Create Memberships table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Memberships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(id)
            )
        ''')

        # Create Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                issue_date TEXT NOT NULL,
                return_date TEXT,
                FOREIGN KEY (user_id) REFERENCES Users(id),
                FOREIGN KEY (book_id) REFERENCES Books(id)
            )
        ''')

        conn.commit()  # Save changes
        print("Tables created successfully!")
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

# Main function to set up the database
def setup_database():
    conn = create_connection()
    if conn:
        create_tables(conn)
        insert_sample_data(conn) 
        conn.close()  # Close the connection

# Run the setup
if __name__ == "__main__":
    setup_database()