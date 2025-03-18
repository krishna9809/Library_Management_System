import sqlite3

# Function to view all transactions
def view_all_transactions():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT Transactions.id, Users.username, Books.title, Transactions.issue_date, Transactions.return_date
                FROM Transactions
                JOIN Users ON Transactions.user_id = Users.id
                JOIN Books ON Transactions.book_id = Books.id
            ''')
            transactions = cursor.fetchall()

            print("\n--- All Transactions ---")
            for transaction in transactions:
                print(f"Transaction ID: {transaction[0]}, User: {transaction[1]}, Book: {transaction[2]}, Issue Date: {transaction[3]}, Return Date: {transaction[4] or 'Not returned'}")
        except sqlite3.Error as e:
            print(f"Error fetching transactions: {e}")
        finally:
            conn.close()

# Function to view overdue books
def view_overdue_books():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT Transactions.id, Users.username, Books.title, Transactions.issue_date
                FROM Transactions
                JOIN Users ON Transactions.user_id = Users.id
                JOIN Books ON Transactions.book_id = Books.id
                WHERE Transactions.return_date IS NULL AND date('now') > date(Transactions.issue_date, '+14 days')
            ''')
            overdue_books = cursor.fetchall()

            print("\n--- Overdue Books ---")
            for book in overdue_books:
                print(f"Transaction ID: {book[0]}, User: {book[1]}, Book: {book[2]}, Issue Date: {book[3]}")
        except sqlite3.Error as e:
            print(f"Error fetching overdue books: {e}")
        finally:
            conn.close()

# Function to create a connection to the SQLite database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('library.db')  # Connect to the database
        print("Connection to SQLite DB successful!")
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite DB: {e}")
    return conn

# Function to display the admin menu
def admin_menu():
    while True:
        print("\n--- Admin Dashboard ---")
        print("1. Add Book")
        print("2. Update Book")
        print("3. Add Membership")
        print("4. Update Membership")
        print("5. View All Books")
        print("6. View All Memberships")
        print("7. View All Transactions")
        print("8. View Overdue Books")
        print("9. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            update_book()
        elif choice == "3":
            add_membership()
        elif choice == "4":
            update_membership()
        elif choice == "5":
            view_all_books()
        elif choice == "6":
            view_all_memberships()
        elif choice == "7":
            view_all_transactions()
        elif choice == "8":
            view_overdue_books()
        elif choice == "9":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

# Function to add a new book
def add_book():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            title = input("Enter book title: ")
            author = input("Enter book author: ")

            cursor.execute('''
                INSERT INTO Books (title, author) VALUES (?, ?)
            ''', (title, author))

            conn.commit()
            print("Book added successfully!")
        except sqlite3.Error as e:
            print(f"Error adding book: {e}")
        finally:
            conn.close()

# Function to update a book
def update_book():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            book_id = input("Enter book ID to update: ")
            title = input("Enter new title: ")
            author = input("Enter new author: ")

            cursor.execute('''
                UPDATE Books SET title = ?, author = ? WHERE id = ?
            ''', (title, author, book_id))

            conn.commit()
            print("Book updated successfully!")
        except sqlite3.Error as e:
            print(f"Error updating book: {e}")
        finally:
            conn.close()

# Function to add a new membership
def add_membership():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            user_id = input("Enter user ID: ")
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")

            cursor.execute('''
                INSERT INTO Memberships (user_id, start_date, end_date) VALUES (?, ?, ?)
            ''', (user_id, start_date, end_date))

            conn.commit()
            print("Membership added successfully!")
        except sqlite3.Error as e:
            print(f"Error adding membership: {e}")
        finally:
            conn.close()

# Function to update a membership
def update_membership():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            membership_id = input("Enter membership ID to update: ")
            start_date = input("Enter new start date (YYYY-MM-DD): ")
            end_date = input("Enter new end date (YYYY-MM-DD): ")

            cursor.execute('''
                UPDATE Memberships SET start_date = ?, end_date = ? WHERE id = ?
            ''', (start_date, end_date, membership_id))

            conn.commit()
            print("Membership updated successfully!")
        except sqlite3.Error as e:
            print(f"Error updating membership: {e}")
        finally:
            conn.close()

# Function to view all books
def view_all_books():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Books')
            books = cursor.fetchall()

            print("\n--- All Books ---")
            for book in books:
                print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Available: {'Yes' if book[3] else 'No'}")
        except sqlite3.Error as e:
            print(f"Error fetching books: {e}")
        finally:
            conn.close()

# Function to view all memberships
def view_all_memberships():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Memberships')
            memberships = cursor.fetchall()

            print("\n--- All Memberships ---")
            for membership in memberships:
                print(f"ID: {membership[0]}, User ID: {membership[1]}, Start Date: {membership[2]}, End Date: {membership[3]}")
        except sqlite3.Error as e:
            print(f"Error fetching memberships: {e}")
        finally:
            conn.close()

# Main function to test the admin dashboard
if __name__ == "__main__":
    admin_menu()