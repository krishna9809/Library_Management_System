import tkinter as tk
from tkinter import messagebox
import sqlite3

# Function to create a connection to the SQLite database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('library.db')
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
            cursor.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()
            if user:
                return user  # Return the user record
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error during login: {e}")
        finally:
            conn.close()

# Login Window
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System - Login")
        self.root.geometry("300x200")

        # Username Label and Entry
        self.label_username = tk.Label(root, text="Username:")
        self.label_username.pack(pady=5)
        self.entry_username = tk.Entry(root)
        self.entry_username.pack(pady=5)

        # Password Label and Entry
        self.label_password = tk.Label(root, text="Password:")
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack(pady=5)

        # Login Button
        self.button_login = tk.Button(root, text="Login", command=self.login)
        self.button_login.pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        user = login(username, password)
        if user:
            self.root.destroy()  # Close the login window
            if user[3] == "admin":
                AdminDashboard()
            else:
                UserDashboard(user[0])  # Pass the user ID to the user dashboard
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

# Admin Dashboard
class AdminDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Library Management System - Admin Dashboard")
        self.root.geometry("400x300")

        # Add Book Button
        self.button_add_book = tk.Button(self.root, text="Add Book", command=self.add_book)
        self.button_add_book.pack(pady=10)

        # Update Book Button
        self.button_update_book = tk.Button(self.root, text="Update Book", command=self.update_book)
        self.button_update_book.pack(pady=10)

        # View All Books Button
        self.button_view_books = tk.Button(self.root, text="View All Books", command=self.view_all_books)
        self.button_view_books.pack(pady=10)

        # Add Membership Button
        self.button_add_membership = tk.Button(self.root, text="Add Membership", command=self.add_membership)
        self.button_add_membership.pack(pady=10)

        # View All Memberships Button
        self.button_view_memberships = tk.Button(self.root, text="View All Memberships", command=self.view_all_memberships)
        self.button_view_memberships.pack(pady=10)

        # View All Transactions Button
        self.button_view_transactions = tk.Button(self.root, text="View All Transactions", command=self.view_all_transactions)
        self.button_view_transactions.pack(pady=10)

        # View Overdue Books Button
        self.button_view_overdue_books = tk.Button(self.root, text="View Overdue Books", command=self.view_overdue_books)
        self.button_view_overdue_books.pack(pady=10)

        # Logout Button
        self.button_logout = tk.Button(self.root, text="Logout", command=self.logout)
        self.button_logout.pack(pady=10)

        self.root.mainloop()

    # Add Book (already implemented)
    def add_book(self):
        # Open a new window to add a book
        add_book_window = tk.Toplevel()
        add_book_window.title("Add Book")
        add_book_window.geometry("300x150")

        # Title Label and Entry
        label_title = tk.Label(add_book_window, text="Title:")
        label_title.pack(pady=5)
        entry_title = tk.Entry(add_book_window)
        entry_title.pack(pady=5)

        # Author Label and Entry
        label_author = tk.Label(add_book_window, text="Author:")
        label_author.pack(pady=5)
        entry_author = tk.Entry(add_book_window)
        entry_author.pack(pady=5)

        # Add Button
        button_add = tk.Button(add_book_window, text="Add", command=lambda: self.save_book(entry_title.get(), entry_author.get(), add_book_window))
        button_add.pack(pady=10)

    def save_book(self, title, author, window):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO Books (title, author) VALUES (?, ?)', (title, author))
                conn.commit()
                messagebox.showinfo("Success", "Book added successfully!")
                window.destroy()  # Close the add book window
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error adding book: {e}")
            finally:
                conn.close()

    # Update Book
    def update_book(self):
        update_book_window = tk.Toplevel()
        update_book_window.title("Update Book")
        update_book_window.geometry("300x200")

        # Book ID Label and Entry
        label_book_id = tk.Label(update_book_window, text="Book ID:")
        label_book_id.pack(pady=5)
        entry_book_id = tk.Entry(update_book_window)
        entry_book_id.pack(pady=5)

        # New Title Label and Entry
        label_new_title = tk.Label(update_book_window, text="New Title:")
        label_new_title.pack(pady=5)
        entry_new_title = tk.Entry(update_book_window)
        entry_new_title.pack(pady=5)

        # New Author Label and Entry
        label_new_author = tk.Label(update_book_window, text="New Author:")
        label_new_author.pack(pady=5)
        entry_new_author = tk.Entry(update_book_window)
        entry_new_author.pack(pady=5)

        # Update Button
        button_update = tk.Button(update_book_window, text="Update", command=lambda: self.save_book_update(entry_book_id.get(), entry_new_title.get(), entry_new_author.get(), update_book_window))
        button_update.pack(pady=10)

    def save_book_update(self, book_id, new_title, new_author, window):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('UPDATE Books SET title = ?, author = ? WHERE id = ?', (new_title, new_author, book_id))
                conn.commit()
                messagebox.showinfo("Success", "Book updated successfully!")
                window.destroy()  # Close the update book window
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error updating book: {e}")
            finally:
                conn.close()

    # View All Books (already implemented)
    def view_all_books(self):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM Books')
                books = cursor.fetchall()

                # Open a new window to display books
                books_window = tk.Toplevel()
                books_window.title("All Books")
                books_window.geometry("400x300")

                # Display books in a listbox
                listbox_books = tk.Listbox(books_window)
                for book in books:
                    listbox_books.insert(tk.END, f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Available: {'Yes' if book[3] else 'No'}")
                listbox_books.pack(fill=tk.BOTH, expand=True)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error fetching books: {e}")
            finally:
                conn.close()

    # Add Membership
    def add_membership(self):
        add_membership_window = tk.Toplevel()
        add_membership_window.title("Add Membership")
        add_membership_window.geometry("300x200")

        # User ID Label and Entry
        label_user_id = tk.Label(add_membership_window, text="User ID:")
        label_user_id.pack(pady=5)
        entry_user_id = tk.Entry(add_membership_window)
        entry_user_id.pack(pady=5)

        # Start Date Label and Entry
        label_start_date = tk.Label(add_membership_window, text="Start Date (YYYY-MM-DD):")
        label_start_date.pack(pady=5)
        entry_start_date = tk.Entry(add_membership_window)
        entry_start_date.pack(pady=5)

        # End Date Label and Entry
        label_end_date = tk.Label(add_membership_window, text="End Date (YYYY-MM-DD):")
        label_end_date.pack(pady=5)
        entry_end_date = tk.Entry(add_membership_window)
        entry_end_date.pack(pady=5)

        # Add Button
        button_add = tk.Button(add_membership_window, text="Add", command=lambda: self.save_membership(entry_user_id.get(), entry_start_date.get(), entry_end_date.get(), add_membership_window))
        button_add.pack(pady=10)

    def save_membership(self, user_id, start_date, end_date, window):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO Memberships (user_id, start_date, end_date) VALUES (?, ?, ?)', (user_id, start_date, end_date))
                conn.commit()
                messagebox.showinfo("Success", "Membership added successfully!")
                window.destroy()  # Close the add membership window
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error adding membership: {e}")
            finally:
                conn.close()

    # View All Memberships
    def view_all_memberships(self):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM Memberships')
                memberships = cursor.fetchall()

                # Open a new window to display memberships
                memberships_window = tk.Toplevel()
                memberships_window.title("All Memberships")
                memberships_window.geometry("400x300")

                # Display memberships in a listbox
                listbox_memberships = tk.Listbox(memberships_window)
                for membership in memberships:
                    listbox_memberships.insert(tk.END, f"ID: {membership[0]}, User ID: {membership[1]}, Start Date: {membership[2]}, End Date: {membership[3]}")
                listbox_memberships.pack(fill=tk.BOTH, expand=True)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error fetching memberships: {e}")
            finally:
                conn.close()

    # View All Transactions
    def view_all_transactions(self):
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

                # Open a new window to display transactions
                transactions_window = tk.Toplevel()
                transactions_window.title("All Transactions")
                transactions_window.geometry("500x300")

                # Display transactions in a listbox
                listbox_transactions = tk.Listbox(transactions_window)
                for transaction in transactions:
                    listbox_transactions.insert(tk.END, f"ID: {transaction[0]}, User: {transaction[1]}, Book: {transaction[2]}, Issue Date: {transaction[3]}, Return Date: {transaction[4] or 'Not returned'}")
                listbox_transactions.pack(fill=tk.BOTH, expand=True)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error fetching transactions: {e}")
            finally:
                conn.close()

    # View Overdue Books
    def view_overdue_books(self):
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

                # Open a new window to display overdue books
                overdue_books_window = tk.Toplevel()
                overdue_books_window.title("Overdue Books")
                overdue_books_window.geometry("500x300")

                # Display overdue books in a listbox
                listbox_overdue_books = tk.Listbox(overdue_books_window)
                for book in overdue_books:
                    listbox_overdue_books.insert(tk.END, f"Transaction ID: {book[0]}, User: {book[1]}, Book: {book[2]}, Issue Date: {book[3]}")
                listbox_overdue_books.pack(fill=tk.BOTH, expand=True)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error fetching overdue books: {e}")
            finally:
                conn.close()

    # Logout
    def logout(self):
        self.root.destroy()  # Close the admin dashboard
        main()  # Reopen the login window


# User Dashboard
class UserDashboard:
    def __init__(self, user_id):
        self.user_id = user_id
        self.root = tk.Tk()
        self.root.title("Library Management System - User Dashboard")
        self.root.geometry("400x300")

        # View Available Books Button
        self.button_view_books = tk.Button(self.root, text="View Available Books", command=self.view_available_books)
        self.button_view_books.pack(pady=10)

        # Issue a Book Button
        self.button_issue_book = tk.Button(self.root, text="Issue a Book", command=self.issue_book)
        self.button_issue_book.pack(pady=10)

        # Return a Book Button
        self.button_return_book = tk.Button(self.root, text="Return a Book", command=self.return_book)
        self.button_return_book.pack(pady=10)

        # View My Transactions Button
        self.button_view_transactions = tk.Button(self.root, text="View My Transactions", command=self.view_my_transactions)
        self.button_view_transactions.pack(pady=10)

        # View My Overdue Books Button
        self.button_view_overdue_books = tk.Button(self.root, text="View My Overdue Books", command=self.view_my_overdue_books)
        self.button_view_overdue_books.pack(pady=10)

        # View My Fines Button
        self.button_view_fines = tk.Button(self.root, text="View My Fines", command=self.view_my_fines)
        self.button_view_fines.pack(pady=10)

        # Logout Button
        self.button_logout = tk.Button(self.root, text="Logout", command=self.logout)
        self.button_logout.pack(pady=10)

        self.root.mainloop()

    # View Available Books (already implemented)
    def view_available_books(self):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM Books WHERE available = 1')
                books = cursor.fetchall()

                # Open a new window to display available books
                books_window = tk.Toplevel()
                books_window.title("Available Books")
                books_window.geometry("400x300")

                # Display books in a listbox
                listbox_books = tk.Listbox(books_window)
                for book in books:
                    listbox_books.insert(tk.END, f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}")
                listbox_books.pack(fill=tk.BOTH, expand=True)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error fetching available books: {e}")
            finally:
                conn.close()

    # Issue a Book
    def issue_book(self):
        issue_book_window = tk.Toplevel()
        issue_book_window.title("Issue a Book")
        issue_book_window.geometry("300x150")

        # Book ID Label and Entry
        label_book_id = tk.Label(issue_book_window, text="Book ID:")
        label_book_id.pack(pady=5)
        entry_book_id = tk.Entry(issue_book_window)
        entry_book_id.pack(pady=5)

        # Issue Button
        button_issue = tk.Button(issue_book_window, text="Issue", command=lambda: self.save_issue_book(entry_book_id.get(), issue_book_window))
        button_issue.pack(pady=10)

def save_issue_book(self, book_id, window):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT available FROM Books WHERE id = ?', (book_id,))
            book = cursor.fetchone()

            if book and book[0] == 1:
                # Use double quotes for the outer string and single quotes for the SQL query
                cursor.execute("INSERT INTO Transactions (user_id, book_id, issue_date) VALUES (?, ?, date('now'))", (self.user_id, book_id))
                cursor.execute('UPDATE Books SET available = 0 WHERE id = ?', (book_id,))
                conn.commit()
                messagebox.showinfo("Success", "Book issued successfully!")
                window.destroy()  # Close the issue book window
            else:
                messagebox.showerror("Error", "Book is not available.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error issuing book: {e}")
        finally:
            conn.close()

    # Return a Book
    def return_book(self):
        return_book_window = tk.Toplevel()
        return_book_window.title("Return a Book")
        return_book_window.geometry("300x150")

        # Book ID Label and Entry
        label_book_id = tk.Label(return_book_window, text="Book ID:")
        label_book_id.pack(pady=5)
        entry_book_id = tk.Entry(return_book_window)
        entry_book_id.pack(pady=5)

        # Return Button
        button_return = tk.Button(return_book_window, text="Return", command=lambda: self.save_return_book(entry_book_id.get(), return_book_window))
        button_return.pack(pady=10)

def save_return_book(self, book_id, window):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM Transactions WHERE user_id = ? AND book_id = ? AND return_date IS NULL', (self.user_id, book_id))
            transaction = cursor.fetchone()

            if transaction:
                # Use double quotes for the outer string and single quotes for the SQL query
                cursor.execute("UPDATE Transactions SET return_date = date('now') WHERE id = ?", (transaction[0],))
                cursor.execute('UPDATE Books SET available = 1 WHERE id = ?', (book_id,))
                conn.commit()
                messagebox.showinfo("Success", "Book returned successfully!")
                window.destroy()  # Close the return book window
            else:
                messagebox.showerror("Error", "No active issue found for this book.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error returning book: {e}")
        finally:
            conn.close()

    # View My Transactions
    def view_my_transactions(self):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT Transactions.id, Books.title, Transactions.issue_date, Transactions.return_date
                    FROM Transactions
                    JOIN Books ON Transactions.book_id = Books.id
                    WHERE Transactions.user_id = ?
                ''', (self.user_id,))
                transactions = cursor.fetchall()

                # Open a new window to display transactions
                transactions_window = tk.Toplevel()
                transactions_window.title("My Transactions")
                transactions_window.geometry("500x300")

                # Display transactions in a listbox
                listbox_transactions = tk.Listbox(transactions_window)
                for transaction in transactions:
                    listbox_transactions.insert(tk.END, f"Transaction ID: {transaction[0]}, Book: {transaction[1]}, Issue Date: {transaction[2]}, Return Date: {transaction[3] or 'Not returned'}")
                listbox_transactions.pack(fill=tk.BOTH, expand=True)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error fetching transactions: {e}")
            finally:
                conn.close()

    # View My Overdue Books
    def view_my_overdue_books(self):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT Transactions.id, Books.title, Transactions.issue_date
                    FROM Transactions
                    JOIN Books ON Transactions.book_id = Books.id
                    WHERE Transactions.user_id = ? AND Transactions.return_date IS NULL AND date('now') > date(Transactions.issue_date, '+14 days')
                ''', (self.user_id,))
                overdue_books = cursor.fetchall()

                # Open a new window to display overdue books
                overdue_books_window = tk.Toplevel()
                overdue_books_window.title("My Overdue Books")
                overdue_books_window.geometry("500x300")

                # Display overdue books in a listbox
                listbox_overdue_books = tk.Listbox(overdue_books_window)
                for book in overdue_books:
                    listbox_overdue_books.insert(tk.END, f"Transaction ID: {book[0]}, Book: {book[1]}, Issue Date: {book[2]}")
                listbox_overdue_books.pack(fill=tk.BOTH, expand=True)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error fetching overdue books: {e}")
            finally:
                conn.close()

    # View My Fines
    def view_my_fines(self):
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
                ''', (self.user_id,))
                fines = cursor.fetchall()

                # Open a new window to display fines
                fines_window = tk.Toplevel()
                fines_window.title("My Fines")
                fines_window.geometry("500x300")

                # Display fines in a listbox
                listbox_fines = tk.Listbox(fines_window)
                for fine in fines:
                    listbox_fines.insert(tk.END, f"Fine ID: {fine[0]}, Book: {fine[1]}, Amount: ${fine[2]}, Payment Date: {fine[3]}")
                listbox_fines.pack(fill=tk.BOTH, expand=True)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error fetching fines: {e}")
            finally:
                conn.close()

    # Logout
    def logout(self):
        self.root.destroy()  # Close the user dashboard
        main()  # Reopen the login window

# Main function to start the application
def main():
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()

# Run the application
if __name__ == "__main__":
    main()