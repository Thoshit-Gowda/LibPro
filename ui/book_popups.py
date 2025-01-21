from tkinter import filedialog
import ttkbootstrap as ttk
import tkinter as tk
from tkinter import StringVar, messagebox
from backend.books import add_book, download_barcodes, update_books, remove_books

def get_selected_book(table):
    selected = table.focus()
    if selected:
        return table.item(selected, "values")
    return None

def open_add_book_popup(app, refresh_table_callback):
    popup = ttk.Toplevel(app)
    popup.geometry("600x400")
    popup.title("Add Book")
    popup.configure(bg="white")

    canvas = tk.Canvas(popup, highlightthickness=0, bg="white")
    canvas.pack(fill="both", expand=True)

    width = 600
    height = 400

    form_frame = ttk.Frame(canvas)
    canvas.create_window(width // 2, height // 2, window=form_frame, anchor="center")
    form_frame.grid_rowconfigure(0, weight=1)

    ttk.Label(form_frame, text="Add Book", font=("Cambria", 18, "bold")).grid(row=0, columnspan=2, pady=20)

    isbn_var = StringVar()
    title_var = StringVar()
    description_var = StringVar()
    category_var = StringVar()
    quantity_var = StringVar()
    author_var = StringVar()
    publisher_var = StringVar()
    language_var = StringVar()

    fields = [
        ("ISBN", isbn_var),
        ("Title", title_var),
        ("Description", description_var),
        ("Category", category_var),
        ("Quantity", quantity_var),
        ("Author", author_var),
        ("Publisher", publisher_var),
        ("Language", language_var),
    ]

    entry_vars = {}

    for i, (label, var) in enumerate(fields):
        row = i // 2
        col = i % 2
        
        entry_vars[label] = var

        ttk.Label(form_frame, text=label, font=("Century Gothic", 8)).grid(row=row + 1, column=col * 2, padx=5, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=var, font=("Century Gothic", 10)).grid(row=row + 1, column=col * 2 + 1, padx=5, pady=5, sticky="ew")

    def handle_add_book():
        try:
            isbn = isbn_var.get().strip()
            title = title_var.get().strip()
            description = description_var.get().strip()
            category = category_var.get().strip()
            quantity = int(quantity_var.get())
            author = author_var.get().strip()
            publisher = publisher_var.get().strip()
            language = language_var.get().strip()

            if not isbn or not title or not description or not category or not author or not publisher or not language:
                messagebox.showerror("Error", "All fields must be filled in.")
                return

            result = add_book(
                ISBN=isbn,
                Title=title,
                Description=description,
                Category=category,
                Quantity=quantity,
                Author=author,
                Publisher=publisher,
                Language=language,
            )

            if result.startswith("Invalid"):
                messagebox.showerror("Error", result)
            elif result.startswith("Book quantity updated") or result.startswith("Book added"):
                messagebox.showinfo("Success", result)
                refresh_table_callback()
                popup.destroy()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid data for Quantity.")

    ttk.Button(form_frame, text="Add Book", command=handle_add_book, style="crimson.TButton").grid(row=len(fields) // 2 + 2, columnspan=2, pady=10)

    ttk.Label(form_frame, text="Fill the details and click 'Add Book' to add the book.", font=("Calibri", 10, "italic")).grid(row=len(fields) // 2 + 3, columnspan=2, pady=10)

def update_book_popup(app, book_data, refresh_table_callback):
    popup = ttk.Toplevel(app)
    popup.geometry("600x400")
    popup.title("Update Book")
    popup.configure(bg="white")

    canvas = tk.Canvas(popup, highlightthickness=0, bg="white")
    canvas.pack(fill="both", expand=True)

    width = 600
    height = 400

    form_frame = ttk.Frame(canvas)
    canvas.create_window(width // 2, height // 2, window=form_frame, anchor="center")
    form_frame.grid_rowconfigure(0, weight=1)

    ttk.Label(form_frame, text="Update Book", font=("Cambria", 18, "bold")).grid(row=0, columnspan=2, pady=20)

    title_var = StringVar(value=book_data.get("Title", ""))
    description_var = StringVar(value=book_data.get("Description", ""))
    category_var = StringVar(value=book_data.get("Category", ""))
    author_var = StringVar(value=book_data.get("Author", ""))
    publisher_var = StringVar(value=book_data.get("Publisher", ""))
    language_var = StringVar(value=book_data.get("Language", ""))

    fields = [
        ("Title", title_var),
        ("Description", description_var),
        ("Category", category_var),
        ("Author", author_var),
        ("Publisher", publisher_var),
        ("Language", language_var),
    ]

    entry_vars = {}

    for i, (label, var) in enumerate(fields):
        row = i // 2
        col = i % 2
        
        entry_vars[label] = var

        ttk.Label(form_frame, text=label, font=("Century Gothic", 8)).grid(row=row + 1, column=col * 2, padx=5, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=var, font=("Century Gothic", 10)).grid(row=row + 1, column=col * 2 + 1, padx=5, pady=5, sticky="ew")

    def save_changes():
        updated_data = {label: var.get().strip() for label, var in entry_vars.items()}
        updated_data["ISBN"] = book_data.get("ISBN", "")
        
        if not updated_data["ISBN"]:
            messagebox.showerror("Error", "ISBN is required.")
            return

        if any(not value for value in updated_data.values()):
            messagebox.showerror("Error", "All fields must be filled in.")
            return

        result = update_books(
            updated_data["ISBN"],
            updated_data["Title"],
            updated_data["Description"],
            updated_data["Category"],
            updated_data["Author"],
            updated_data["Publisher"],
            updated_data["Language"]
        )

        if result.startswith("Invalid"):
            messagebox.showerror("Error", result)
        elif result.startswith("Book details updated"):
            messagebox.showinfo("Success", result)
            refresh_table_callback()
            popup.destroy()

    ttk.Button(form_frame, text="Save Changes", command=save_changes, style="crimson.TButton").grid(row=len(fields) // 2 + 2, columnspan=2, pady=10)

    ttk.Label(form_frame, text="Modify the details and click 'Save Changes' to update the book.", font=("Calibri", 10, "italic")).grid(row=len(fields) // 2 + 3, columnspan=2, pady=10)

def open_delete_book_popup(app, table, refresh_table_callback):
    selected_item = table.selection()
    if not selected_item:
        messagebox.showerror("Error", "No book selected!")
        return

    popup = ttk.Toplevel(app)
    popup.geometry("300x300")
    popup.title("Delete Book")
    popup.configure(bg="white")

    canvas = tk.Canvas(popup, highlightthickness=0, bg="white")
    canvas.pack(fill="both", expand=True)

    width, height = 300, 300

    form_frame = ttk.Frame(canvas)
    canvas.create_window(width // 2, height // 2, window=form_frame, anchor="center")
    form_frame.grid_rowconfigure(0, weight=1)

    ttk.Label(form_frame, text="Enter SKU no. to delete.", font=("Cambria", 8, "bold")).grid(row=0, columnspan=2, pady=20)
    sku_var = ttk.StringVar()

    ttk.Label(form_frame, text="SKU:", font=("Century Gothic", 8)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    sku_entry = ttk.Entry(form_frame, textvariable=sku_var, font=("Century Gothic", 10))
    sku_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    def delete_book_by_sku():
        sku_number = sku_var.get().strip()

        if not sku_number:
            messagebox.showerror("Error", "Please enter a valid SKU number.")
            return

        try:
            sku_list = table.item(selected_item)["values"][6].split(",")
            sku = sku_list[int(sku_number) - 1]

            result = remove_books(sku)

            if result == "No Book found" or result == "SKU not found in the book's SKU list":
                messagebox.showerror("Error", result)
            else:
                messagebox.showinfo("Success", "Book deleted successfully!")
                refresh_table_callback()
            popup.destroy()

        except IndexError:
            messagebox.showerror("Error", "Invalid SKU number. Please enter a valid SKU index.")
        except ValueError:
            messagebox.showerror("Error", "Invalid SKU number. Please enter a valid number.")

    def delete_all_books():
        res = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete all books?")

        if res:
            isbn = table.item(selected_item)["values"][1]
            deletion_result = remove_books(isbn, delete_all=True)

            if deletion_result == "All books with ISBN removed successfully":
                messagebox.showinfo("Success", "All books deleted successfully!")
                popup.destroy()
                refresh_table_callback()
            else:
                messagebox.showerror("Error", deletion_result)

    ttk.Button(form_frame, text="Delete SKU", command=delete_book_by_sku, style="crimson.TButton").grid(row=2, columnspan=2, pady=10)
    ttk.Button(form_frame, text="Delete All", command=delete_all_books, style="crimson.TButton").grid(row=3, columnspan=2, pady=10)

    ttk.Label(form_frame, text="This action cannot be undone.", font=("Calibri", 10, "italic")).grid(row=4, columnspan=2, pady=10)

def open_download_barcodes_popup(app, table):
    selected_item = table.selection()
    if not selected_item:
        messagebox.showerror("Error", "No book selected!")
        return
    
    selected_book = table.item(selected_item)["values"]
    if not selected_book:
        messagebox.showerror("Error", "Unable to retrieve selected book data!")
        return
    
    book = {
        "ISBN": selected_book[0],
        "Title": str(selected_book[1]),  
        "SKU": {sku: "date" for sku in selected_book[6].split(",")}
    }
    
    confirm = messagebox.askyesno("Confirmation", f"Do you want to download barcodes for '{book['Title']}'?")
    if not confirm:
        return
    
    save_file = filedialog.asksaveasfilename(
        title="Save Barcode PDF",
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        initialfile=f"{book['Title'].replace(' ', '_')}_barcodes.pdf"
    )

    if save_file:
        result = download_barcodes(book, save_path=save_file)
    else:
        result = download_barcodes(book)
    if result.startswith("Success"):
        messagebox.showinfo("Success", result)
    else:
        messagebox.showerror("Error", result)
