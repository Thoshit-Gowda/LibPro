from tkinter import messagebox
import ttkbootstrap as ttk
from backend.books import get_book_det
from backend.inventory import get_book_inv
from backend.account import wishlist_mem, get_user
from backend.reviews import get_reviews

ACCENT_COLOR = "#dc143c"

def wishlist(app, member,db):

    def show_main_page():
        Books = []
        wishlisted_books = get_user(db=db, email=member, fields={"WishlistedBooks"})
        for book in wishlisted_books:
                Books = book.split(",")
        if wishlisted_books == "No records found." or Books[0] == "": Books = []

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
        
        if len(Books)>0:
            idx = 0
            for book in Books:
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
                    text=f"{get_book_det(isbn=book)[0][2]}\t\t\t\t\t\t\t\t\t\t",
                    font=("Helvetica", 14, "bold"),
                    foreground=ACCENT_COLOR,
                    wraplength=172,
                    anchor="center"
                )
                title_label.pack(padx=5, expand=True, fill="both", anchor="center", side="top")
                title_label.bind("<Button-1>", lambda e, isbn=book: show_details_page(isbn))

                description_label = ttk.Label(
                    book_frame,
                    text=f"Description: {get_book_det(isbn=book)[0][3]}",
                    font=("Helvetica", 10),
                    wraplength=200, 
                    justify="left"
                )
                description_label.pack(padx=5, expand=True, fill="both")
                description_label.bind("<Button-1>", lambda e, isbn=book: show_details_page(isbn))

                author_label = ttk.Label(
                    book_frame,
                    text=f"Author: {get_book_det(isbn=book)[0][4]}",
                    font=("Helvetica", 10)
                )
                author_label.pack(padx=5, expand=True, fill="both")
                author_label.bind("<Button-1>", lambda e, isbn=book: show_details_page(isbn))

                book_frame.bind("<Button-1>", lambda e, isbn=book: show_details_page(isbn))

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

        header = ttk.Frame(details_frame, padding=20)
        header.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        ttk.Label(
            header,
            text="Book Details",
            font=("Century Gothic", 40, "bold"),
            anchor="center",
        ).pack(pady=10)

        ttk.Label(
            header,
            text="Detailed Information about the selected book.",
            font=("Arial", 18, "italic"),
            anchor="center",
        ).pack(pady=5)

        main_panel = ttk.Frame(details_frame, padding=20)
        main_panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)

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

        book = next((b for b in get_book_det() if b[1] == isbn), None)
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
                
                reviewer_email = review[3]
                review_text = review[5]
                rating = review[4]

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

        remove_from_wishlist_button = ttk.Button(
            scrollable_frame,
            text="Remove from Wishlist",
            command=lambda:remove_from_wishlist(member, isbn),
            style="crimson.TButton",
        )
        remove_from_wishlist_button.pack(pady=20)

        back_button = ttk.Button(
            scrollable_frame,
            text="Back",
            command=show_main_page,
            style="crimson.TButton",
        )
        back_button.pack(pady=30)

        def remove_from_wishlist(email, isbn):
            res = wishlist_mem(email ,isbn, action="remove")
            if "Error:" in res:
                messagebox.showerror("Error", res)
            else:
                messagebox.showinfo("Wishlist", f"{isbn} removed from wishlist successfully!")
                show_main_page()

    show_main_page()

    # global show_main_page
    # def show_main_page():
    #     def go_to_dashboard():
    #         main_frame.pack_forget()
    #         #dashboard.welcome_screen(app, member)
    
    #     #for widget in app.winfo_children():
    #     #    widget.destroy()

    #     main_frame = ttk.Frame(app, padding=30)
    #     main_frame.pack(fill="both", expand=True)

    #     left_panel = ttk.Frame(main_frame, padding=20)
    #     left_panel.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    #     ttk.Label(left_panel, text="Your Wishlist", font=("Century Gothic", 40, "bold"), anchor="center").pack(pady=10)
    #     ttk.Label(left_panel, text="Your favourite/saved books!", font=("Arial", 18, "italic"), anchor="center").pack(pady=0)
    #     back_button = ttk.Button(
    #         left_panel,
    #         text="Back to Dashboard",
    #         command=go_to_dashboard,
    #         style="crimson.TButton",
    #     )
    #     back_button.pack(pady=60)

    #     right_panel = ttk.Frame(main_frame, padding=20)
    #     right_panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    #     canvas = ttk.Canvas(right_panel, highlightthickness=0)
    #     scrollbar = ttk.Scrollbar(right_panel, orient="vertical", command=canvas.yview)
    #     scrollable_frame = ttk.Frame(canvas)

    #     scrollable_frame.bind(
    #         "<Configure>",
    #         lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
    #     )
    #     canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    #     canvas.configure(yscrollcommand=scrollbar.set)

    #     canvas.pack(side="left", fill="both", expand=True)
    #     scrollbar.pack(side="right", fill="y")

    #     style = ttk.Style()
    #     style.configure('hover.TFrame', background='#f0f0f0', borderwidth=0)

        
    #     if len(member["Wishlist"])>0:
    #         for isbn in member["Wishlist"]:
    #             book = get_book_det(isbn = isbn)
    #             book_frame = ttk.Frame(scrollable_frame, padding=10, style="default.TFrame")
    #             book_frame.pack(fill="x", pady=(0, 1))

    #             def on_hover(e, frame=book_frame):
    #                 frame.configure(style="hover.TFrame")

    #             def on_leave(e, frame=book_frame):
    #                 frame.configure(style="default.TFrame")

    #             book_frame.bind("<Enter>", on_hover)
    #             book_frame.bind("<Leave>", on_leave)

                
    #             wishlist_label = ttk.Label(
    #                 book_frame,
    #                 text=book["Title"],
    #                 font=("Helvetica", 14, "bold"),
    #                 foreground=ACCENT_COLOR,
    #                 anchor="w"
    #             )
    #             wishlist_label.pack(anchor="w", padx=5)
    #             wishlist_label.bind("<Button-1>", lambda e, isbn=book["ISBN"]: show_details_page(isbn))

    #             isbn_label = ttk.Label(
    #                 book_frame,
    #                 text=f"ISBN: {book['ISBN']}",
    #                 font=("Helvetica", 10),
    #                 anchor="w"
    #             )
    #             isbn_label.pack(anchor="w", padx=5)
    #             isbn_label.bind("<Button-1>", lambda e, isbn=book["ISBN"]: show_details_page(isbn))

    #             book_frame.bind("<Button-1>", lambda e, isbn=book["ISBN"]: show_details_page(isbn))
    #     else:
    #         ttk.Label(
    #             scrollable_frame,
    #             text="No book added to wishlist.",
    #             font=("Helvetica", 14, "bold"),
    #         ).pack(anchor="w", padx=5)


    # def show_details_page(isbn):
    #     for widget in app.winfo_children():
    #         widget.destroy()

    #     details_frame = ttk.Frame(app, padding=30)
    #     details_frame.pack(fill="both", expand=True)

    #     left_panel = ttk.Frame(details_frame, padding=20)
    #     left_panel.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    #     ttk.Label(
    #         left_panel,
    #         text="Book Details",
    #         font=("Century Gothic", 40, "bold"),
    #         anchor="center",
    #     ).pack(pady=10)

    #     ttk.Label(
    #         left_panel,
    #         text="Detailed Information about this wishlisted book.",
    #         font=("Arial", 18, "italic"),
    #         anchor="center",
    #     ).pack(pady=5)

    #     right_panel = ttk.Frame(details_frame, padding=20)
    #     right_panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    #     canvas = ttk.Canvas(right_panel, highlightthickness=0)
    #     scrollbar = ttk.Scrollbar(right_panel, orient="vertical", command=canvas.yview)
    #     scrollable_frame = ttk.Frame(canvas)

    #     scrollable_frame.bind(
    #         "<Configure>",
    #         lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
    #     )
    #     canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    #     canvas.configure(yscrollcommand=scrollbar.set)

    #     canvas.pack(side="left", fill="both", expand=True)
    #     scrollbar.pack(side="right", fill="y")

    #     isbn = next((b for b in member["Wishlist"] if b == isbn), None)
    #     if not isbn:
    #         messagebox.showerror("Error", "Book not found.")
    #         show_main_page()
    #         return
        
    #     book = get_book_det(isbn = isbn)
    #     book_details = [
    #         ("Title", book["Title"]),
    #         ("ISBN", book["ISBN"]),
    #         ("Description", book["Description"]),
    #         ("Category", book["Category"]),
    #         ("Quantity", book["Quantity"]),
    #         ("Author", book["Author"]),
    #         ("Publisher", book["Publisher"]),
    #         ("Language", book["Language"]),
    #     ]

    #     for label, adetail in book_details:
    #         detail_frame = ttk.Frame(scrollable_frame, padding=10)
    #         detail_frame.pack(fill="x", pady=(0, 1))
                        
    #         detail = adetail

    #         if label == "Quantity":
    #             if int(detail) == 0:
    #                 detail = "All copies have been borrowed."
    #             else:
    #                 detail = f"{detail} copies in library."
           
    #         ttk.Label(
    #             detail_frame,
    #             text=f"{label}: {detail}",
    #             font=("Helvetica", 12),
    #             anchor="w",
    #             wraplength=350
    #         ).pack(anchor="w", padx=5)

    #     wishlist_button = ttk.Button(
    #         scrollable_frame,
    #         text="Remove from Wishlist",
    #         command=lambda:remove_from_wishlist(member["UID"], isbn),
    #         style="crimson.TButton",
    #     )
    #     wishlist_button.pack(pady=20)

    #     back_button = ttk.Button(
    #         scrollable_frame,
    #         text="Back",
    #         command=show_main_page,
    #         style="crimson.TButton",
    #     )
    #     back_button.pack(pady=30)

    
