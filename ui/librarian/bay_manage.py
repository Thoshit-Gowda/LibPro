import tkinter as tk
from tkinter import StringVar, ttk, messagebox
from backend.inventory import get_book_inv

def bay_manager(app):
    
    outer_canvas = tk.Canvas(app, bg="#1e1e1e", highlightthickness=0)
    outer_canvas.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

    outer_scroll = ttk.Scrollbar(app, orient=tk.HORIZONTAL, command=outer_canvas.xview, style="Dark.Horizontal.TScrollbar")
    outer_canvas.configure(xscrollcommand=outer_scroll.set)
    outer_scroll.pack(fill=tk.X, side=tk.BOTTOM)

    outer_frame = tk.Frame(outer_canvas, bg="#1e1e1e")
    outer_canvas.create_window((0, 0), window=outer_frame, anchor="nw")

    outer_frame_id = outer_canvas.create_window((0, 0), window=outer_frame, anchor="nw")

    def resize_outer_frame(event):
        outer_canvas.itemconfig(outer_frame_id, height=event.height)
    
    outer_canvas.bind("<Configure>", resize_outer_frame)


    books = get_book_inv()
    bay_map = {}
    for book in books:
        bay_map.setdefault(book[5], []).append(book)

    for bay_index, bay_books in sorted(bay_map.items()):
        # Container frame for scrollable bay
        bay_scroll_frame = tk.Frame(outer_frame, bg="#1e1e1e")
        bay_scroll_frame.pack(side=tk.LEFT, padx=30, fill=tk.Y, expand=True)
    
        # Canvas inside container for vertical scrolling
        bay_canvas = tk.Canvas(bay_scroll_frame, width=280, height=500, bg="#1e1e1e", highlightthickness=0)
        bay_canvas.pack(side=tk.LEFT, fill=tk.Y, expand=True)
    
        # Vertical scrollbar for bay
        bay_v_scroll = ttk.Scrollbar(bay_scroll_frame, orient=tk.VERTICAL, command=bay_canvas.yview, style="Dark.Vertical.TScrollbar")
        bay_v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
        bay_canvas.configure(yscrollcommand=bay_v_scroll.set)
    
        # Create the bay_frame inside the canvas
        bay_frame = tk.Frame(bay_canvas, bg="white", width=280)
        bay_canvas.create_window((0, 0), window=bay_frame, anchor="nw")
    
        tk.Label(bay_frame, text=f"Bay {bay_index}", font=("Arial", 12, "bold"), bg="white").pack(pady=5)
    
        # Group books by shelf
        shelf_map = {}
        max_shelf_index = 0
        for book in bay_books:
            shelf_index = book[6]
            shelf_map.setdefault(shelf_index, []).append(book)
            max_shelf_index = max(max_shelf_index, shelf_index)
    
        # Go through all possible shelf numbers, including empty ones
        for shelf_index in range(max_shelf_index + 1):
            shelf_books = shelf_map.get(shelf_index, [])
            shelf_canvas_frame = tk.Frame(bay_frame, bg="#e0e0e0", height=220,bd=1,relief="solid",highlightbackground="#cccccc",highlightthickness=1)
            shelf_canvas_frame.pack(fill=tk.X, pady=10)
    
            label = tk.Label(shelf_canvas_frame, text=f"Shelf {shelf_index + 1}",
                             font=("Arial", 9, "bold"), bg="#e0e0e0", anchor="w")
            label.pack(fill=tk.X)
    
            shelf_canvas = tk.Canvas(shelf_canvas_frame, width=240, height=180,
                                     bg="#e0e0e0", highlightthickness=0)
            shelf_canvas.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
            row_height, col_width = 30, 60
            padding = 10
    
            if shelf_books:
                for book in shelf_books:
                    row, col = book[7], book[8]
                    x0 = col * col_width + padding
                    y0 = row * row_height + padding
                    x1 = x0 + col_width
                    y1 = y0 + row_height
                    shelf_canvas.create_rectangle(x0, y0, x1, y1, fill="lightgreen", outline="black")
                    shelf_canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2,
                                             text=book[4], font=("Arial", 8), width=col_width - 4)
            else:
                shelf_canvas.create_text(120, 90, text="No books", font=("Arial", 10, "italic"), fill="gray")
    
                shelf_canvas.config(scrollregion=shelf_canvas.bbox("all"))
    
        # Update scrollregion for bay_canvas
        bay_frame.update_idletasks()
        bay_canvas.config(scrollregion=bay_canvas.bbox("all"))
    
        # Enable mousewheel vertical scrolling inside bay_canvas
        def on_enter(event, canvas=bay_canvas):
           canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        def on_leave(event, canvas=bay_canvas):
            canvas.unbind_all("<MouseWheel>")
        
        bay_canvas.bind("<Enter>", on_enter)
        bay_canvas.bind("<Leave>", on_leave)
        
    


    outer_frame.update_idletasks()
    outer_canvas.config(scrollregion=outer_canvas.bbox("all"))
