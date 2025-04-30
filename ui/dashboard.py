from tkinter import ttk, messagebox
from ui.book_popups import open_add_book_popup, open_download_barcodes_popup, update_book_popup, open_delete_book_popup
from backend.books import Books, read_book

def admin_dashboard(app, user):
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return

    header = ttk.Frame(app)
    header.pack(fill="x")

    label = ttk.Label(header, text="Hello, "f"{user}!", font=("Gotham Bold", 20, "bold"))
    label.pack(side="left", padx=10, pady=25)

    stats_frame = ttk.Frame(app, height=100)
    stats_frame.pack(fill="x", pady=50)

    users_frame = ttk.Frame(stats_frame, height=100, width=100,style="My.TFrame")
    users_frame.pack(padx=50, fill="y")

    users_label = ttk.Label(users_frame, text="Total Users")
    users_label.pack(expand=True)

    books_frame = ttk.Frame(stats_frame, height=100, width=100, style="My.TFrame")
    users_frame.pack(padx=50, fill="y")

    books_label = ttk.Label(books_frame, text="Total Books")
    books_label.pack(expand=True)