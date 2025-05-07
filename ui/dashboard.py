import time
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from ui.book_popups import open_add_book_popup, open_download_barcodes_popup, update_book_popup, open_delete_book_popup

from backend.books import Books, read_book, available_books
from backend.members import borrowed_books, overdue_books, total_overdue_books
from backend.utils import load_data, MEMBERS_FILE

from ui.client.view_books import view_books
from ui.client.view_borrowed_books import view_borrowed_books
from ui.client.wishlist import wishlist

Members = load_data(MEMBERS_FILE)

ADMIN_CREDENTIALS =[{
   "Name": "Pratham",
   "Password": "123"
   },{
    "Name": "Thejas",
    "Password": "456"
   },{
    "Name": "Thoshit",
    "Password": "789"
   }]

def update_time(label):
    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%A, %B %d, %Y")
    label.config(text=f"{current_time}, {current_date}")
    label.after(1000, update_time, label)

def dashboard(app, user):
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return

    column_widths = {
           "SKU": 40,
           "ID": 40,
           "Member": 90,
           "Title": 110,
           "Author": 90,
           "Overdue": 60,
           "Return Date": 90,
           "Fine to be Paid": 40
        }

    ttk.Label(app, text="Hello,"f'{user["Name"]}!', font=("Helvetica", 20, "bold"), foreground="#4682B4").pack(anchor="w", padx=20, pady=(10, 0))
    time_label = ttk.Label(app, font=("Helvetica", 10))
    time_label.pack(anchor="w", padx=20)
    update_time(time_label)

    summary_frame = ttk.Frame(app)
    summary_frame.pack(fill=X, padx=20, pady=20)

    content_frame = ttk.Frame(app)
    content_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

    books_frame = ttk.Labelframe(content_frame, text="Overdue Books", padding=10, width=500)
    books_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
    books_frame.pack_propagate(0)
    
    def create_card(parent, title, value):
        frame = ttk.Frame(parent, style="secondary.TFrame")
        frame.pack(side=LEFT, expand=True, fill=BOTH, padx=10)
        ttk.Label(frame, text=title, font=("Helvetica", 10), background="#4682B4").pack()
        ttk.Label(frame, text=value, font=("Helvetica", 18, "bold"), background="#4682B4").pack()
    
    if user in ADMIN_CREDENTIALS and user not in Members:
        create_card(summary_frame, "Borrowed Books", f"{borrowed_books}")
        create_card(summary_frame, "Overdue Books", f"{total_overdue_books()}")
        create_card(summary_frame, "Total Visitors", f"{len(Members)}")
        create_card(summary_frame, "Available Books",f"{available_books}")
 
        books_tree = ttk.Treeview(
         books_frame,
         columns=("ID", "Member", "Title", "Author", "Overdue", "Return Date"),
         show="headings"
        )   
 
        for col in books_tree["columns"]:
            books_tree.heading(col, text=col)
            books_tree.column(col, anchor='center', minwidth=80, width=column_widths[col], stretch=True)
    
        books_tree.pack(fill=BOTH, expand=True)

        books_tree.insert("", "end", values=(
            "",                # Id
            "",              # Member
            "",               # Title
            "",      # Author
            "",             # Overdue
            ""          # Return Date (ISO format recommended)
        ))
    
        books_tree.insert("", "end", values=(
           "B001",                # Id
           "Alice",              # Member
           "1984",               # Title
           "George Orwell",      # Author
           "5 days",             # Overdue
           "2025-05-10"          # Return Date (ISO format recommended)
        ))

    elif user not in ADMIN_CREDENTIALS and user in Members:
        create_card(summary_frame, "Overdue Books", f"{overdue_books(user["UID"])}")
        create_card(summary_frame, "Borrowed Books", f"{len(user["SKU"])}")
        create_card(summary_frame, "BookMarks", f"{user["BookMarks"]}")
        create_card(summary_frame, "Available Books",f"{available_books}")
 
        books_tree = ttk.Treeview(
         books_frame,
         columns=("SKU", "Title", "Author", "Overdue", "Return Date", "Fine to be Paid"),
         show="headings"
        )
 
        for col in books_tree["columns"]:
            books_tree.heading(col, text=col)
            books_tree.column(col, anchor='center', minwidth=80, width=column_widths[col], stretch=True)
     
        books_tree.pack(fill=BOTH, expand=True)

        books_tree.insert("", "end", values=(
            "",                # Id
            "",              # Member
            "",               # Title
            "",      # Author
            "",             # Overdue
            ""          # Return Date (ISO format recommended)
        ))
    
        books_tree.insert("", "end", values=(
            "B001",                # Id
            "1984",               # Title
            "George Orwell",      # Author
            "5 days",             # Overdue
            "2025-05-10",        # Return Date (ISO format recommended)
            "Rs20"
        ))

    else: return("Unknown User")
