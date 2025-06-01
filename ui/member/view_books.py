from tkinter import messagebox
import ttkbootstrap as ttk
from backend.books import get_book_det
from backend.account import wishlist_mem
from backend.inventory import get_book_inv
from backend.reviews import get_reviews

ACCENT_COLOR = "#6CA6CD"

def add_to_wishlist(email, isbn):
    res = wishlist_mem(True,email,isbn)
    if "Error:" in res:
        messagebox.showerror("Error", res)
    else:
        messagebox.showinfo("Wishlist", f"{isbn} added to wishlist successfully!")

Books = get_book_det()

def view_books(app, email):
    def show_main_page():
        main_frame = ttk.Frame(app, padding=30)
        main_frame.pack(fill="both", expand=True)

        #left_panel = ttk.Frame(main_frame, padding=20)
        #left_panel.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        #ttk.Label(left_panel, text="Available Books", font=("Century Gothic", 40, "bold"), anchor="center").pack(pady=10)
        #ttk.Label(left_panel, text="List of Books available in this library.", font=("Arial", 18, "italic"), anchor="center").pack(pady=0)

        right_panel = ttk.Frame(main_frame, padding=20)
        right_panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        canvas = ttk.Canvas(right_panel, highlightthickness=0)
        scrollbar = ttk.Scrollbar(right_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        style = ttk.Style()
        style.configure('hover.TFrame', background='#f0f0f0', borderwidth=0)
        
        if len(Books)>0:
            idx = 0
            for book in Books:
                row = idx // 4
                col = idx % 4
                idx = idx + 1
                book_frame = ttk.Frame(scrollable_frame, width=100, height=150,borderwidth=3, bootstyle="dark")
                book_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                book_frame.grid_propagate(False)  

                def on_hover(e, frame=book_frame):
                    frame.configure(style="hover.TFrame")

                def on_leave(e, frame=book_frame):
                    frame.configure(bootstyle="dark")

                book_frame.bind("<Enter>", on_hover)
                book_frame.bind("<Leave>", on_leave)

                title_label = ttk.Label(
                    book_frame,
                    text=f"{book[2]}\t\t\t\t\t\t\t\t\t\t",
                    font=("Helvetica", 14, "bold"),
                    foreground=ACCENT_COLOR,
                    wraplength=172 
                )
                title_label.pack(padx=5, expand=True, fill="both")
                title_label.bind("<Button-1>", lambda e, isbn=book[1]: show_details_page(isbn))

                description_label = ttk.Label(
                    book_frame,
                    text=f"Description: {book[3]}",
                    font=("Helvetica", 10),
                    wraplength=200, 
                    justify="left"
                )
                description_label.pack(padx=5, expand=True, fill="both")
                description_label.bind("<Button-1>", lambda e, isbn=book[1]: show_details_page(isbn))

                author_label = ttk.Label(
                    book_frame,
                    text=f"Author: {book[4]}",
                    font=("Helvetica", 10)
                )
                author_label.pack(padx=5, expand=True, fill="both")
                author_label.bind("<Button-1>", lambda e, isbn=book[1]: show_details_page(isbn))

                book_frame.bind("<Button-1>", lambda e, isbn=book[1]: show_details_page(isbn))

            for i in range(4):
                scrollable_frame.grid_columnconfigure(i, weight=1)

        else:
            ttk.Label(
                scrollable_frame,
                text="No books found.",
                font=("Helvetica", 14, "bold"),
            ).pack(anchor="w", padx=5)
            


    def show_details_page(isbn):
        for widget in app.winfo_children():
            widget.destroy()

        details_frame = ttk.Frame(app, padding=30)
        details_frame.pack(fill="both", expand=True)

        left_panel = ttk.Frame(details_frame, padding=20)
        left_panel.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        ttk.Label(
            left_panel,
            text="Book Details",
            font=("Century Gothic", 40, "bold"),
            anchor="center",
        ).pack(pady=10)

        ttk.Label(
            left_panel,
            text="Detailed Information about the selected book.",
            font=("Arial", 18, "italic"),
            anchor="center",
        ).pack(pady=5)

        right_panel = ttk.Frame(details_frame, padding=20)
        right_panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        canvas = ttk.Canvas(right_panel, highlightthickness=0)
        scrollbar = ttk.Scrollbar(right_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        book = next((b for b in Books if b[1] == isbn), None)
        if not book:
            messagebox.showerror("Error", "Book not found.")
            show_main_page()
            return

        book_details = [
            ("ISBN", book[1]),
            ("Title", book[2]),
            ("Description", book[3]),
            ("Author", book[4]),
            ("Publication", book[5]),
            ("Genre", book[6]),
            ("Language", book[7]),
            ("Added On", book[8]),
            ("Updated On", book[9]),
        ]

        for label, adetail in book_details:
            detail_frame = ttk.Frame(scrollable_frame, padding=10)
            detail_frame.pack(fill="x", pady=(0, 1))
                        
            detail = adetail

            ttk.Label(
                detail_frame,
                text=f"{label}: {detail}",
                font=("Helvetica", 12),
                anchor="w",
                wraplength=350
            ).pack(anchor="w", padx=5)
        
        qty = get_book_inv(isbn=isbn, count=True)
        no = "All copies have been borrowed."
        if qty > 0:
            no = f"{qty} copies in library."

        ttk.Label(
            detail_frame,
            text=f"Quantity: {no}",
            font=("Helvetica", 12),
            anchor="w",
            wraplength=350
        ).pack(anchor="w", padx=5)

        reviews = get_reviews(isbn)
        review_frame = ttk.Frame(scrollable_frame, padding=10)
        review_frame.pack(fill="x", pady=(0, 1))
        if reviews!="No reviews found for this book.":
            for review in reviews:

                reviewer_email = review[1]
                review_text = review[2]
                rating = review[3]

                ttk.Label(
                    review_frame,
                    text=f"Reviewer: {reviewer_email}",
                    font=("Helvetica", 12),
                    anchor="w",
                    wraplength=350
                ).pack(anchor="w", padx=5)

                ttk.Label(
                    review_frame,
                    text=f"Rating: {rating}/5",
                    font=("Helvetica", 12),
                    anchor="w",
                    wraplength=350
                ).pack(anchor="w", padx=5)

                ttk.Label(
                    review_frame,
                    text=f"Review: {review_text}",
                    font=("Helvetica", 12),
                    anchor="w",
                    wraplength=350
                ).pack(anchor="w", padx=5)
        else:
            ttk.Label(
                review_frame,
                text=f"No Reviews found for this book.",
                font=("Helvetica", 12),
                anchor="w",
                wraplength=350
            ).pack(anchor="w", padx=5)
        
        ttk.Label(
            detail_frame,
            text=f"{label}: {detail}",
            font=("Helvetica", 12),
            anchor="w",
            wraplength=350
        ).pack(anchor="w", padx=5)

        wishlist_button = ttk.Button(
            scrollable_frame,
            text="Add to Wishlist",
            command=lambda:add_to_wishlist(email, isbn),
            style="crimson.TButton",
        )
        wishlist_button.pack(pady=20)

        back_button = ttk.Button(
            scrollable_frame,
            text="Back",
            command=show_main_page,
            style="crimson.TButton",
        )
        back_button.pack(pady=30)

    show_main_page()
