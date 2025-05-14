import ttkbootstrap as ttk
from tkinter import messagebox
from ttkbootstrap.constants import *
from backend.account import get_user
from backend.bookrecord import get_record, overdue_books
from backend.inventory import get_book_inv
from backend.utils import update_time
from ui.common import create_card


column_widths = {
        "SKU": 40,
        "ID": 40,
        "Member": 90,
        "Days Borrowed": 90,
        "Days Overdue": 60,
        "Return Date": 90,
        "Fine(Rs.)": 40
    }

def dashboard_content(app, email, db):
    if not app and db not in ["Librarian", "Members"]:
        messagebox.showerror("Error", "Application instance not found / database error.")
        return
    
    userDet = get_user(db, email=email)

    ttk.Label(app, text="Hello, "f'{userDet[2]}.', font=("Helvetica", 20, "bold"), foreground="#4682B4").pack(anchor="w", padx=20, pady=(10, 0))
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

    if db == "Librarian":
        create_card(summary_frame, "Borrowed Books", f"{get_record(status="Borrowed",count=True)}")
        create_card(summary_frame, "Overdue Books", f"{overdue_books(count=True)}")
        create_card(summary_frame, "Members Count", f"{get_user(db="Members", count=True)}")
        create_card(summary_frame, "Available Books",f"{get_book_inv(count=True)}")
    
        books_tree = ttk.Treeview(
        books_frame,
        columns=("SKU", "Member", "Days Overdue", "Return Date", "Fine(Rs.)"),
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

        books_tree.insert("", "end", values=overdue_books())

    elif db=="Members":
        create_card(summary_frame, "Overdue Books", f"{overdue_books(email=email,count=True)}")
        create_card(summary_frame, "Borrowed Books", f"{get_record(email=email, status="Borrowed", count=True)}")
        create_card(summary_frame, "ProPoints ", f"{userDet[6]}")
        create_card(summary_frame, "Available Books",f"{get_book_inv(count=True)}")
 
        books_tree = ttk.Treeview(
         books_frame,
         columns=("SKU", "Days Borrowed", "Days Overdue", "Return Date", "Fine(Rs.)"),
         show="headings"
        )
 
        for col in books_tree["columns"]:
            books_tree.heading(col, text=col)
            books_tree.column(col, anchor='center', minwidth=80, width=column_widths[col], stretch=True)
     
        books_tree.pack(fill=BOTH, expand=True)

        books_tree.insert("", "end", values=(
            "",     
            "",     
            "",     
            "",     
            "",     
            ""      
        ))

        for rec in overdue_books(email=email):
                books_tree.insert("", "end", values=rec)
        
