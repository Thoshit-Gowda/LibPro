from datetime import datetime
import ttkbootstrap as ttk
from tkinter import messagebox
from backend.bookrecord import get_record
from backend.books import get_book_det

ACCENT_COLOR = "#dc143c"

def view_borrowed_books(app, member):

    brrwd_books = get_record(email=member)

    def show_main_page():
        for widget in app.winfo_children():
            widget.destroy()
            
        main_frame = ttk.Frame(app, padding=30)
        main_frame.pack(fill="both", expand=True)

        main_panel = ttk.Frame(main_frame, padding=20)
        main_panel.pack(side="top", fill="both", expand=True, padx=20, anchor="n")

        canvas = ttk.Canvas(main_panel, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_panel, orient="vertical", command=canvas.yview)
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
        
        if len(brrwd_books)>0:
            idx = 0
            for book in brrwd_books:
                row = idx // 4
                col = idx % 4
                idx = idx + 1
                book_frame = ttk.Frame(scrollable_frame, width=100, height=160,borderwidth=3, bootstyle="dark")
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
                    text=f"{get_book_det(isbn=book[2])[0][2]}\t\t\t\t\t\t\t\t\t\t",
                    font=("Helvetica", 14, "bold"),
                    foreground=ACCENT_COLOR,
                    wraplength=172,
                    anchor="center"
                )
                title_label.pack(padx=5, expand=True, fill="both", anchor="center", side="top")
                title_label.bind("<Button-1>", lambda e, sku=book[0]: show_details_page(sku))

                description_label = ttk.Label(
                    book_frame,
                    text=f"Description: {get_book_det(isbn=book[2])[0][3]}",
                    font=("Helvetica", 10),
                    wraplength=200, 
                    justify="left"
                )
                description_label.pack(padx=5, expand=True, fill="both")
                description_label.bind("<Button-1>", lambda e, sku=book[0]: show_details_page(sku))

                author_label = ttk.Label(
                    book_frame,
                    text=f"Author: {get_book_det(isbn=book[2])[0][4]}",
                    font=("Helvetica", 10)
                )
                author_label.pack(padx=5, expand=True, fill="both")
                author_label.bind("<Button-1>", lambda e, sku=book[0]: show_details_page(sku))

                book_frame.bind("<Button-1>", lambda e, sku=book[0]: show_details_page(sku))

            for i in range(4):
                scrollable_frame.grid_columnconfigure(i, weight=1)

        else:
            ttk.Label(
                scrollable_frame,
                text="No books found.",
                font=("Helvetica", 14, "bold"),
            ).pack(anchor="w", padx=5)

    def show_details_page(sku):
        for widget in app.winfo_children():
            widget.destroy()
    
        book = next((b for b in brrwd_books if b[0] == sku), None)
        if not book:
            messagebox.showerror("Error", "Book not found.")
            show_main_page()
            return

        container = ttk.Frame(app, padding=20)
        container.pack(fill="both", expand=True)
    
        # Book Details Frame (Left)
        details_frame = ttk.Frame(container, padding=10)
        details_frame.pack(side="left", fill="both", expand=True)
    
        ttk.Label(
            details_frame,
            text="Borrowed Book Details",
            font=("Century Gothic", 18, "bold")
        ).pack(pady=(0, 15))
    
        details = [
            ("SKU", book[0]),
            ("Status", book[1]),
            ("ISBN", book[2]),
            ("Title", book[2]),
            ("Author", book[4]),
            ("Borrower", f"{book[4]} ({book[3]})"),
            ("Borrowed On", book[6]),
            ("Returned On", book[11] if book[11] else "Not returned yet"),
            ("Fine (Rs.)", book[9]),
            ("Genre", book[6]),
            ("Language", book[7]),
        ]
    
        for label, value in details:
            frame = ttk.Frame(details_frame, padding=5)
            frame.pack(fill="x")
            ttk.Label(frame, text=f"{label}:", font=("Helvetica", 11, "bold"), width=15, anchor="w").pack(side="left")
            ttk.Label(frame, text=value, font=("Helvetica", 11), anchor="w", wraplength=300).pack(side="left", fill="x", expand=True)
    
        # Review Frame (Right)
        review_frame = ttk.Frame(container, padding=10)
        review_frame.pack(side="left", fill="both", expand=True)
    
        ttk.Label(
            review_frame,
            text="Write a Review",
            font=("Helvetica", 16, "bold"),
        ).pack(anchor="w", pady=(0, 10))
    
        review_text = ttk.Text(review_frame, height=6, width=50, wrap="word")
        review_text.pack(fill="x", pady=(0, 10))
    
        ttk.Label(
            review_frame,
            text="Rating (1 to 5):",
            font=("Helvetica", 11)
        ).pack(anchor="w", pady=(5, 2))
    
        rating_var = ttk.StringVar(value="5")
        rating_menu = ttk.Combobox(
            review_frame,
            textvariable=rating_var,
            values=["1", "2", "3", "4", "5"],
            width=5,
            state="readonly",
        )
        rating_menu.pack(anchor="w", pady=(0, 10))
    
        def submit_review():
            review = review_text.get("1.0", "end").strip()
            rating = rating_var.get()
    
            from backend.reviews import add_review
    
            response = add_review(
                isbn=book[2],
                fullname=book[4],  # Assuming book[4] is FullName
                email=book[3],     # Assuming book[3] is Email
                review=review,
                rating=rating
            )
    
            if response == "Review added successfully.":
                messagebox.showinfo("Success", response)
                review_text.delete("1.0", "end")
                rating_var.set("5")
            else:
                messagebox.showerror("Error", response)
    
        ttk.Button(
            review_frame,
            text="Submit Review",
            command=submit_review,
            bootstyle="success-outline"
        ).pack(anchor="center", pady=15)

        ttk.Button(
            details_frame,
            text="Back",
            command=show_main_page,
            bootstyle="secondary-outline"
        ).pack(pady=20, anchor="w")




        # book = next((b for b in brrwd_books if b[1] == isbn), None)
        # if not book:
        #     messagebox.showerror("Error", "Book not found.")
        #     show_main_page()
        #     return

        # book_details = [
        #     ("ISBN", book[1]),
        #     ("Title", book[2]),
        #     ("Description", book[3]),
        #     ("Author", book[4]),
        #     ("Publication", book[5]),
        #     ("Genre", book[6]),
        #     ("Language", book[7]),
        #     ("Added On", book[8]),
        #     ("Updated On", book[9]),
        # ]

        # for label, adetail in book_details:
        #     detail_frame = ttk.Frame(scrollable_frame, padding=10)
        #     detail_frame.pack(fill="x", pady=(0, 1))
                        
        #     detail = adetail

        #     ttk.Label(
        #         detail_frame,
        #         text=f"{label}: {detail}",
        #         font=("Helvetica", 12),
        #         anchor="w",
        #         wraplength=350
        #     ).pack(anchor="w", padx=5)
        
        # qty = get_book_inv(isbn=isbn, count=True)
        # no = "All copies have been borrowed."
        # if qty > 0:
        #     no = f"{qty} copies in library."

        # ttk.Label(
        #     detail_frame,
        #     text=f"Quantity: {no}",
        #     font=("Helvetica", 12),
        #     anchor="w",
        #     wraplength=350
        # ).pack(anchor="w", padx=5)

        # reviews = get_reviews(isbn)
        # review_frame = ttk.Frame(scrollable_frame, padding=10)
        # review_frame.pack(fill="x", pady=(0, 1))
        # if reviews!="No reviews found for this book.":
        #     for review in reviews:

        #         reviewer_email = review[1]
        #         review_text = review[2]
        #         rating = review[3]

        #         ttk.Label(
        #             review_frame,
        #             text=f"Reviewer: {reviewer_email}",
        #             font=("Helvetica", 12),
        #             anchor="w",
        #             wraplength=350
        #         ).pack(anchor="w", padx=5)

        #         ttk.Label(
        #             review_frame,
        #             text=f"Rating: {rating}/5",
        #             font=("Helvetica", 12),
        #             anchor="w",
        #             wraplength=350
        #         ).pack(anchor="w", padx=5)

        #         ttk.Label(
        #             review_frame,
        #             text=f"Review: {review_text}",
        #             font=("Helvetica", 12),
        #             anchor="w",
        #             wraplength=350
        #         ).pack(anchor="w", padx=5)
        # else:
        #     ttk.Label(
        #         review_frame,
        #         text=f"No Reviews found for this book.",
        #         font=("Helvetica", 12),
        #         anchor="w",
        #         wraplength=350
        #     ).pack(anchor="w", padx=5)
        
        # ttk.Label(
        #     detail_frame,
        #     text=f"{label}: {detail}",
        #     font=("Helvetica", 12),
        #     anchor="w",
        #     wraplength=350
        # ).pack(anchor="w", padx=5)

        # wishlist_button = ttk.Button(
        #     scrollable_frame,
        #     text="Add to Wishlist",
        #     command=lambda:add_to_wishlist(email, isbn),
        #     style="crimson.TButton",
        # )
        # wishlist_button.pack(pady=20)

        # back_button = ttk.Button(
        #     scrollable_frame,
        #     text="Back",
        #     command=show_main_page,
        #     style="crimson.TButton",
        # )
        # back_button.pack(pady=30)

    show_main_page()
