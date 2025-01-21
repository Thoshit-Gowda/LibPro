import tkinter as tk
from tkinter import StringVar, ttk, messagebox
from backend.shelfing import deshelve, search, shelf, categorise, BookShelf, DeshelvedBooks
from backend.utils import open_barcode_scanner

def back_to_dashboard(app):    
    from ui.dashboard import welcome_screen
    
    for widget in app.winfo_children():
        widget.grid_forget()

    welcome_screen(app)

def show_deshelved_books():
    if not DeshelvedBooks:
        messagebox.showinfo("Deshelved Books", "No books have been deshelved.")
    else:
        books_list = "\n".join([f"SKU: {sku}, {details}" for sku, details in DeshelvedBooks.items()])
        messagebox.showinfo("Deshelved Books", f"Deshelved Books:\n\n{books_list}")


def open_shelve_popup(app, update_shelf_view):
    def shelve_book():
        try:
            rack = int(rack_entry.get())
            shelf_num = int(shelf_entry.get())
            sku = sku_entry.get()

            if not sku:
                raise ValueError("SKU cannot be empty.")

            result = shelf(rack, shelf_num, sku)
            messagebox.showinfo("Success", result)

            update_shelf_view()
            popup.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    popup = tk.Toplevel(app)
    popup.title("Shelve Book")

    tk.Label(popup, text="Rack Number").grid(row=0, column=0, padx=10, pady=5)
    rack_entry = tk.Entry(popup)
    rack_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(popup, text="Shelf Number").grid(row=1, column=0, padx=10, pady=5)
    shelf_entry = tk.Entry(popup)
    shelf_entry.grid(row=1, column=1, padx=10, pady=5)

    sku_var = StringVar()
    tk.Label(popup, text="SKU").grid(row=2, column=0, padx=10, pady=5)
    sku_entry = tk.Entry(popup, textvariable=sku_var)
    sku_entry.grid(row=2, column=1, padx=10, pady=5)

    def start_scanning():
        open_barcode_scanner(sku_var) 
    ttk.Button(popup, text="Scan Barcode", command=start_scanning, style="crimson.TButton").grid(row=3, column=0, columnspan=2, pady=20)

    ttk.Button(popup, text="Submit", command=shelve_book, style="crimson.TButton").grid(row=4, column=0, columnspan=2, pady=20)


def open_search_popup(app):
    def search_book():
        sku = sku_entry.get()

        if not sku:
            messagebox.showerror("Error", "SKU cannot be empty.")
            return

        result = search(sku)
        if "Error" in result:
            messagebox.showerror("Error", result)
        else:
            messagebox.showinfo("Success", result)
            popup.destroy()

    popup = tk.Toplevel(app)
    popup.title("Search Book")
    sku_var = StringVar()

    tk.Label(popup, text="Enter SKU").grid(row=0, column=0, padx=10, pady=5)
    sku_entry = tk.Entry(popup, textvariable=sku_var)
    sku_entry.grid(row=0, column=1, padx=10, pady=5)
    def start_scanning():
        open_barcode_scanner(sku_var) 
    ttk.Button(popup, text="Scan Barcode", command=start_scanning, style="crimson.TButton").grid(row=1, column=0, columnspan=2, pady=20)

    ttk.Button(popup, text="Search", command=search_book, style="crimson.TButton").grid(row=2, column=0, columnspan=2, pady=20)


def open_deshelve_popup(app, update_shelf_view):
    sku_var = StringVar()
    def deshelve_book():
        sku = sku_entry.get()

        if not sku:
            messagebox.showerror("Error", "SKU cannot be empty.")
            return

        result = deshelve(sku)
        if "Error" in result:
            messagebox.showerror("Error", result)
        else:
            messagebox.showinfo("Success", result)

        update_shelf_view()
        popup.destroy()

    popup = tk.Toplevel(app)
    popup.title("Deshelve Book")
    def start_scanning():
        open_barcode_scanner(sku_var) 

    tk.Label(popup, text="Enter SKU").grid(row=0, column=0, padx=10, pady=5)
    sku_entry = tk.Entry(popup, textvariable=sku_var)
    sku_entry.grid(row=0, column=1, padx=10, pady=5)

    ttk.Button(popup, text="Scan Barcode", command=start_scanning, style="crimson.TButton").grid(row=1, column=0, columnspan=2, pady=20)
    ttk.Button(popup, text="Deshelve", command=deshelve_book, style="crimson.TButton").grid(row=2, column=0, columnspan=2, pady=10)


def open_categorise_popup(app, update_shelf_view):
    def categorise_book():
        try:
            rack = int(rack_entry.get())
            shelf_num = int(shelf_entry.get())
            category = category_entry.get()

            if not category:
                raise ValueError("Category cannot be empty.")

            result = categorise(rack, shelf_num, category)
            messagebox.showinfo("Success", result)

            update_shelf_view()
            popup.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    popup = tk.Toplevel(app)
    popup.title("Categorize Book")

    tk.Label(popup, text="Rack Number").grid(row=0, column=0, padx=10, pady=5)
    rack_entry = tk.Entry(popup)
    rack_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(popup, text="Shelf Number").grid(row=1, column=0, padx=10, pady=5)
    shelf_entry = tk.Entry(popup)
    shelf_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(popup, text="Category").grid(row=2, column=0, padx=10, pady=5)
    category_entry = tk.Entry(popup)
    category_entry.grid(row=2, column=1, padx=10, pady=5)

    ttk.Button(popup, text="Submit", command=categorise_book, style="crimson.TButton").grid(row=3, column=0, columnspan=2, pady=10)


def shelf_manage(app):
    def update_shelf_view():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        if not BookShelf:
            no_rack_label = ttk.Label(scrollable_frame, text="No rack found!", font=("Arial", 16, "bold"))
            no_rack_label.grid(row=0, column=0, padx=10, pady=10)
            return

        row = 0
        col = 0
        max_columns = 3

        for rack_number, categories in enumerate(BookShelf, 1):
            rack_frame = ttk.Frame(scrollable_frame, padding=10, relief="solid", width=200, height=300)
            rack_frame.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")

            rack_label = ttk.Label(rack_frame, text=f"Rack {rack_number}", font=("Arial", 14, "bold"))
            rack_label.grid(row=0, column=0, padx=10, pady=5)

            shelf_row = 1
            for category_dict in categories:
                if category_dict:
                    for category_name, skus in category_dict.items():
                        shelf_frame = ttk.Frame(rack_frame, padding=10, relief="groove")
                        shelf_frame.grid(row=shelf_row, column=0, padx=5, pady=5, sticky="nsew")

                        shelf_label = ttk.Label(shelf_frame, text=category_name, font=("Arial", 12))
                        shelf_label.grid(row=0, column=0, padx=5, pady=5)

                        table_frame = ttk.Frame(shelf_frame)
                        table_frame.grid(row=1, column=0, padx=5, pady=5)

                        columns = ("SKU",)
                        table = ttk.Treeview(table_frame, columns=columns, show="headings", height=4)
                        table.grid(row=0, column=0, sticky="nsew")

                        table.heading("SKU", text="SKU")

                        for sku in skus:
                            table.insert("", "end", values=(sku,))

                        shelf_row += 1

            col += 1
            if col >= max_columns:
                col = 0
                row += 1

        scrollable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    paned_window = ttk.PanedWindow(app, orient="horizontal")
    paned_window.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    left_frame = ttk.Frame(paned_window)
    paned_window.add(left_frame, weight=4)

    right_frame = ttk.Frame(paned_window, width=200)
    paned_window.add(right_frame, weight=1)

    canvas = tk.Canvas(left_frame)
    canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    scrollable_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)

    left_frame.grid_rowconfigure(0, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    ttk.Button(right_frame, text="Categorize Book", command=lambda: open_categorise_popup(app, update_shelf_view), style="crimson.TButton").grid(row=0, column=0, pady=10)
    ttk.Button(right_frame, text="Shelve Book", command=lambda: open_shelve_popup(app,update_shelf_view), style="crimson.TButton").grid(row=1, column=0, pady=10)
    ttk.Button(right_frame, text="Search Book", command=lambda: open_search_popup(app), style="crimson.TButton").grid(row=2, column=0, pady=10)
    ttk.Button(right_frame, text="Deshelve Book", command=lambda: open_deshelve_popup(app,update_shelf_view), style="crimson.TButton").grid(row=3, column=0, pady=10)
    ttk.Button(right_frame, text="View Deshelved Books", command=lambda: show_deshelved_books(), style="crimson.TButton").grid(row=4, column=0, pady=10)
    ttk.Button(right_frame, text="Dashboard", command=lambda: back_to_dashboard(app), style="crimson.TButton").grid(row=5, column=0, pady=50)

    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)

    update_shelf_view()
