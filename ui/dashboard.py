import time
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ui.book_popups import open_add_book_popup, open_download_barcodes_popup, update_book_popup, open_delete_book_popup
from backend.books import Books, read_book, available_books
from backend.members import borrowed_books
from backend.utils import load_data, MEMBERS_FILE

Members = load_data(MEMBERS_FILE)

def admin_dashboard(app, user):
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return

    ttk.Label(app, text="Hello,"f'{user}', font=("Helvetica", 20, "bold"), foreground="red").pack(anchor="w", padx=20, pady=(10, 0))
    time_label = ttk.Label(app, text="Time", font=("Helvetica", 10)).pack(anchor="w", padx=20)
    
    # Summary cards
    summary_frame = ttk.Frame(app)
    summary_frame.pack(fill=X, padx=20, pady=20)
    
    def create_card(parent, title, value):
        frame = ttk.Frame(parent, padding=15, style="secondary.TFrame")
        frame.pack(side=LEFT, expand=True, fill=BOTH, padx=10)
        ttk.Label(frame, text=value, font=("Helvetica", 18, "bold")).pack()
        ttk.Label(frame, text=title, font=("Helvetica", 10)).pack()
    
    # Placeholder cards
    create_card(summary_frame, "Total Visitors", f"{len(Members)}")
    create_card(summary_frame, "Borrowed Books", f"{borrowed_books}")
    create_card(summary_frame, "Overdue Books", "----")
    create_card(summary_frame, "Available Books",f"{available_books}")
    
    # Main content section
    content_frame = ttk.Frame(app)
    content_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
    
    # Users List
    user_frame = ttk.Labelframe(content_frame, text="Users List", padding=10, width=500)
    user_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
    user_frame.pack_propagate(0)
    
    ttk.Button(user_frame, text="Add New User").pack(anchor='e', pady=5)
    
    user_tree = ttk.Treeview(user_frame, columns=("User ID", "User Name", "Book Issued"), show="headings")
    for col in user_tree["columns"]:
        user_tree.heading(col, text=col)
        user_tree.column(col, anchor='center')
    user_tree.pack(fill=BOTH, expand=True)
    
    # Books List
    books_frame = ttk.Labelframe(content_frame, text="Books List", padding=10, width=500)
    books_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
    books_frame.pack_propagate(0)
    
    ttk.Button(books_frame, text="Add New Book").pack(anchor='e', pady=5)
    
    books_tree = ttk.Treeview(books_frame, columns=("Book ID", "Title", "Available"), show="headings")
    for col in books_tree["columns"]:
        books_tree.heading(col, text=col)
        books_tree.column(col, anchor='center')
    books_tree.pack(fill=BOTH, expand=True)