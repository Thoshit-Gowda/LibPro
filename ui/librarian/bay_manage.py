import tkinter as tk
from tkinter import StringVar, ttk, messagebox
from backend.inventory import get_book_inv


def draw_bay(canvas, bay_books, bay_index):
    shelf_height, row_height, col_width = 160, 20, 60
    padding = 20
    text_color = "white"

    max_shelf = max(b[6] for b in bay_books)
    max_row = max(b[7] for b in bay_books)
    max_col = max(b[8] for b in bay_books)

    for book in bay_books:
        shelf, row, col = book[6], book[7], book[8]
        x0 = col * col_width + padding
        y0 = shelf * shelf_height + row * row_height + padding + 20  # Push down to leave room for shelf label
        x1 = x0 + col_width
        y1 = y0 + row_height
        canvas.create_rectangle(x0, y0, x1, y1, fill="lightgreen", outline="black")
        canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=book[4], font=("Arial", 8), fill=text_color, width=col_width - 4)

    # Draw shelf labels (above shelf area)
    for shelf in range(max_shelf + 1):
        y = shelf * shelf_height + padding
        canvas.create_text(padding, y + 5, anchor="w", text=f"Shelf {shelf + 1}", font=("Arial", 9, "bold"), fill=text_color)

    canvas.create_text(padding, 10, anchor="w", text=f"Bay {bay_index + 1}", font=("Arial", 10, "bold"), fill=text_color)

    canvas.config(scrollregion=canvas.bbox("all"))

def bay_manager(app):
    
    #def update_shelf_view():
    #    for widget in scrollable_frame.winfo_children():
    #        widget.destroy()
#
    #    if not BookShelf:
    #        no_bay_label = ttk.Label(scrollable_frame, text="No bay found!", font=("Arial", 16, "bold"))
    #        no_bay_label.grid(row=0, column=0, padx=10, pady=10)
    #        return
#
    #    row = 0
    #    col = 0
    #    max_columns = 3
#
    #    for bay_number, categories in enumerate(BookShelf, 1):
    #        bay_frame = ttk.Frame(scrollable_frame, padding=10, relief="solid", width=200, height=300)
    #        bay_frame.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
#
    #        bay_label = ttk.Label(bay_frame, text=f"bay {bay_number}", font=("Arial", 14, "bold"))
    #        bay_label.grid(row=0, column=0, padx=10, pady=5)
#
    #        shelf_row = 1
    #        for category_dict in categories:
    #            if category_dict:
    #                for category_name, skus in category_dict.items():
    #                    shelf_frame = ttk.Frame(bay_frame, padding=10, relief="groove")
    #                    shelf_frame.grid(row=shelf_row, column=0, padx=5, pady=5, sticky="nsew")
#
    #                    shelf_label = ttk.Label(shelf_frame, text=category_name, font=("Arial", 12))
    #                    shelf_label.grid(row=0, column=0, padx=5, pady=5)
#
    #                    table_frame = ttk.Frame(shelf_frame)
    #                    table_frame.grid(row=1, column=0, padx=5, pady=5)
#
    #                    columns = ("SKU",)
    #                    table = ttk.Treeview(table_frame, columns=columns, show="headings", height=4)
    #                    table.grid(row=0, column=0, sticky="nsew")
#
    #                    table.heading("SKU", text="SKU")
#
    #                    for sku in skus:
    #                        table.insert("", "end", values=(sku,))
#
    #                    shelf_row += 1
#
    #        col += 1
    #        if col >= max_columns:
    #            col = 0
    #            row += 1
#
    #    scrollable_frame.update_idletasks()
    #    canvas.config(scrollregion=canvas.bbox("all"))
#
    #paned_window = ttk.PanedWindow(app, orient="horizontal")
    #paned_window.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
#
    #left_frame = ttk.Frame(paned_window)
    #paned_window.add(left_frame, weight=4)
#
    #right_frame = ttk.Frame(paned_window, width=200)
    #paned_window.add(right_frame, weight=1)
#
    #canvas = tk.Canvas(left_frame)
    #canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
#
    #scrollable_frame = ttk.Frame(canvas)
    #canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
#
    #scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
    #scrollbar.grid(row=0, column=1, sticky="ns")
    #canvas.configure(yscrollcommand=scrollbar.set)
#
    #left_frame.grid_rowconfigure(0, weight=1)
    #left_frame.grid_columnconfigure(0, weight=1)
#
    #ttk.Button(right_frame, text="Categorize Book", command=lambda: open_categorise_popup(app, update_shelf_view), style="crimson.TButton").grid(row=0, column=0, pady=10)
    #ttk.Button(right_frame, text="Shelve Book", command=lambda: open_shelve_popup(app,update_shelf_view), style="crimson.TButton").grid(row=1, column=0, pady=10)
    #ttk.Button(right_frame, text="Search Book", command=lambda: open_search_popup(app), style="crimson.TButton").grid(row=2, column=0, pady=10)
    #ttk.Button(right_frame, text="Deshelve Book", command=lambda: open_deshelve_popup(app,update_shelf_view), style="crimson.TButton").grid(row=3, column=0, pady=10)
    #ttk.Button(right_frame, text="View Deshelved Books", command=lambda: show_deshelved_books(), style="crimson.TButton").grid(row=4, column=0, pady=10)
#
    #app.grid_rowconfigure(0, weight=1)
    #app.grid_columnconfigure(0, weight=1)
#
    #update_shelf_view()
 



    # Dummy function definitions for database simulation
    

    
    outer_canvas = tk.Canvas(app, bg="#1e1e1e", highlightthickness=0)
    outer_canvas.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

    outer_scroll = tk.Scrollbar(app, orient=tk.HORIZONTAL, command=outer_canvas.xview)
    outer_canvas.configure(xscrollcommand=outer_scroll.set)
    outer_scroll.pack(fill=tk.X, side=tk.BOTTOM)

    outer_frame = tk.Frame(outer_canvas, bg="#1e1e1e")
    outer_canvas.create_window((0, 0), window=outer_frame, anchor="nw")

    books = get_book_inv()
    bay_map = {}
    for book in books:
        bay_map.setdefault(book[5], []).append(book)

    for bay_index, bay_books in sorted(bay_map.items()):
        bay_frame = tk.Frame(outer_frame, width=240, height=700, bg="#1e1e1e")
        bay_frame.pack(side=tk.LEFT, padx=20)

        bay_canvas = tk.Canvas(bay_frame, width=240, height=700, bg="#1e1e1e", highlightthickness=0)
        bay_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scroll = tk.Scrollbar(bay_frame, orient=tk.VERTICAL, command=bay_canvas.yview)
        bay_canvas.configure(yscrollcommand=v_scroll.set)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        v_scroll.configure(troughcolor="#1e1e1e", bg="#1e1e1e", highlightthickness=0, width=2)

        draw_bay(bay_canvas, bay_books, bay_index)

        bay_canvas.update_idletasks()
        bay_canvas.config(scrollregion=bay_canvas.bbox("all"))

    outer_frame.update_idletasks()
    outer_canvas.config(scrollregion=outer_canvas.bbox("all"))
