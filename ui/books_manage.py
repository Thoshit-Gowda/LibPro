from tkinter import ttk, messagebox
from ui.book_popups import open_add_book_popup, open_download_barcodes_popup, update_book_popup, open_delete_book_popup
from backend.books import Books, read_book

def books_manage(app):
    global table, table_frame

    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return

    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    table_frame = ttk.Frame(app)
    table_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    table_frame.grid_columnconfigure(0, weight=1)

    columns = ("ID", "ISBN", "Title", "Description", "Category", "Quantity", "SKU", "Author", "Language", "Publisher")
    table = ttk.Treeview(table_frame, columns=columns, show="headings", height=40)

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=100, anchor="center", stretch=True)

    scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=table.xview)
    table.configure(xscrollcommand=scrollbar.set)
    scrollbar.grid(row=1, column=0, sticky="ew")

    table.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

    button_frame = ttk.Frame(app)
    button_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
    button_frame.grid_columnconfigure(0, weight=1)

    ttk.Button(button_frame, text="Add Book", command=lambda: open_add_book_popup(app, display_books), style="crimson.TButton").pack(fill="x", pady=5)
    ttk.Button(button_frame, text="Update Book", command=lambda: open_update_book_popup(app), style="crimson.TButton").pack(fill="x", pady=5)
    ttk.Button(button_frame, text="Delete Book", command=lambda: open_delete_book_popup(app, table, display_books), style="crimson.TButton").pack(fill="x", pady=5)
    ttk.Button(button_frame, text="Download Barcode", command=lambda: open_download_barcodes_popup(app, table), style="crimson.TButton").pack(fill="x", pady=5)

    app.grid_columnconfigure(0, weight=3)
    app.grid_columnconfigure(1, weight=1)

    display_books()

def open_update_book_popup(app):
    selected_item = table.selection()
    if not selected_item:
        messagebox.showerror("Error", "No book selected!")
        return

    ISBN = str(table.item(selected_item)["values"][1]) 
    book = read_book(ISBN) 

    if isinstance(book, str):
        messagebox.showerror("Error", "Book not found!")
        return

    update_book_popup(app, book, display_books)

def display_books():
    for row in table.get_children():
        table.delete(row)

    for index, book in enumerate(Books):
        table.insert("", "end", values=( 
            index + 1,
            book["ISBN"],
            book["Title"],
            book["Description"],
            book["Category"],
            book["Quantity"],
            ", ".join(book["SKU"].keys()),
            book["Author"],
            book["Language"],
            book["Publisher"],
        ))

def update_table(table):
    for row in table.get_children():
        table.delete(row)

    for book in Books:
        table.insert("", "end", values=(book["ISBN"], book["Title"], book["Author"], book["Quantity"]))
