import sqlite3

# Function to view fine details for the logged-in user
def view_my_fines(user_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT Payments.id, Books.title, Payments.amount, Payments.payment_date
                FROM Payments
                JOIN Transactions ON Payments.transaction_id = Transactions.id
                JOIN Books ON Transactions.book_id = Books.id
                WHERE Payments.user_id = ?
            ''', (user_id,))
            fines = cursor.fetchall()

            print("\n--- My Fines ---")
            for fine in fines:
                print(f"Fine ID: {fine[0]}, Book: {fine[1]}, Amount: ${fine[2]}, Payment Date: {fine[3]}")
        except sqlite3.Error as e:
            print(f"Error fetching fines: {e}")
        finally:
            conn.close()

# Function to view overdue books for the logged-in user
def view_my_overdue_books(user_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT Transactions.id, Books.title, Transactions.issue_date
                FROM Transactions
                JOIN Books ON Transactions.book_id = Books.id
                WHERE Transactions.user_id = ? AND Transactions.return_date IS NULL AND date('now') > date(Transactions.issue_date, '+14 days')
            ''', (user_id,))
            overdue_books = cursor.fetchall()

            print("\n--- My Overdue Books ---")
            for book in overdue_books:
                print(f"Transaction ID: {book[0]}, Book: {book[1]}, Issue Date: {book[2]}")
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

# Function to display the user menu
def user_menu(user_id):
    while True:
        print("\n--- User Dashboard ---")
        print("1. View Available Books")
        print("2. Issue a Book")
        print("3. Return a Book")
        print("4. View My Transactions")
        print("5. View My Overdue Books")
        print("6. View My Fines")
        print("7. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_available_books()
        elif choice == "2":
            issue_book(user_id)
        elif choice == "3":
            return_book(user_id)
        elif choice == "4":
            view_my_transactions(user_id)
        elif choice == "5":
            view_my_overdue_books(user_id)
        elif choice == "6":
            view_my_fines(user_id)
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

# Function to view available books
def view_available_books():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Books WHERE available = 1')
            books = cursor.fetchall()

            print("\n--- Available Books ---")
            for book in books:
                print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}")
        except sqlite3.Error as e:
            print(f"Error fetching available books: {e}")
        finally:
            conn.close()

# Function to issue a book
def issue_book(user_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            book_id = input("Enter book ID to issue: ")

            # Check if the book is available
            cursor.execute('SELECT available FROM Books WHERE id = ?', (book_id,))
            book = cursor.fetchone()

            if book and book[0] == 1:
                cursor.execute('''
                    INSERT INTO Transactions (user_id, book_id, issue_date)
                    VALUES (?, ?, date('now'))
                ''', (user_id, book_id))

                cursor.execute('UPDATE Books SET available = 0 WHERE id = ?', (book_id,))
                conn.commit()
                print("Book issued successfully!")
            else:
                print("Book is not available.")
        except sqlite3.Error as e:
            print(f"Error issuing book: {e}")
        finally:
            conn.close()

# Function to return a book
def return_book(user_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            book_id = input("Enter book ID to return: ")

            # Check if the book is issued to the user
            cursor.execute('''
                SELECT id, issue_date FROM Transactions
                WHERE user_id = ? AND book_id = ? AND return_date IS NULL
            ''', (user_id, book_id))

            transaction = cursor.fetchone()

            if transaction:
                transaction_id, issue_date = transaction

                # Calculate fine if the book is overdue
                cursor.execute('''
                    SELECT date('now') > date(?, '+14 days')
                ''', (issue_date,))
                is_overdue = cursor.fetchone()[0]

                fine_amount = 0
                if is_overdue:
                    # Calculate the number of overdue days
                    cursor.execute('''
                        SELECT julianday('now') - julianday(?, '+14 days')
                    ''', (issue_date,))
                    overdue_days = int(cursor.fetchone()[0])
                    fine_amount = overdue_days * 10  # Assuming a fine of $10 per day

                    print(f"\nBook is overdue by {overdue_days} days. Fine: ${fine_amount}")

                # Update the return date in the Transactions table
                cursor.execute('''
                    UPDATE Transactions SET return_date = date('now')
                    WHERE id = ?
                ''', (transaction_id,))

                # Update the book's availability
                cursor.execute('UPDATE Books SET available = 1 WHERE id = ?', (book_id,))

                # Insert fine details into the Payments table (optional)
                if fine_amount > 0:
                    cursor.execute('''
                        INSERT INTO Payments (user_id, transaction_id, amount, payment_date)
                        VALUES (?, ?, ?, date('now'))
                    ''', (user_id, transaction_id, fine_amount))

                conn.commit()
                print("Book returned successfully!")
            else:
                print("No active issue found for this book.")
        except sqlite3.Error as e:
            print(f"Error returning book: {e}")
        finally:
            conn.close()

# Function to view user's transactions
def view_my_transactions(user_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT Transactions.id, Books.title, Transactions.issue_date, Transactions.return_date
                FROM Transactions
                JOIN Books ON Transactions.book_id = Books.id
                WHERE Transactions.user_id = ?
            ''', (user_id,))

            transactions = cursor.fetchall()

            print("\n--- My Transactions ---")
            for transaction in transactions:
                print(f"Transaction ID: {transaction[0]}, Book: {transaction[1]}, Issue Date: {transaction[2]}, Return Date: {transaction[3] or 'Not returned'}")
        except sqlite3.Error as e:
            print(f"Error fetching transactions: {e}")
        finally:
            conn.close()

# Main function to test the user dashboard
if __name__ == "__main__":
    user_id = 2  # Replace with the logged-in user's ID
    user_menu(user_id)