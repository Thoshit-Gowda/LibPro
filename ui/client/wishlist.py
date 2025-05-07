from tkinter import messagebox
import ttkbootstrap as ttk
from backend.books import read_book
from backend.members import manage_wishlist

ACCENT_COLOR = "#dc143c"


def remove_from_wishlist(uid, isbn):
    res = manage_wishlist(False,uid,isbn)
    if "Error:" in res:
        messagebox.showerror("Error", res)
    else:
        messagebox.showinfo("Wishlist", f"{isbn} removed from wishlist successfully!")
        show_main_page()

def wishlist(app, member):
    global show_main_page
    def show_main_page():
        def go_to_dashboard():
            main_frame.pack_forget()

        main_frame = ttk.Frame(app, padding=30)
        main_frame.pack(fill="both", expand=True)

        left_panel = ttk.Frame(main_frame, padding=20)
        left_panel.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        ttk.Label(left_panel, text="Your Wishlist", font=("Century Gothic", 40, "bold"), anchor="center").pack(pady=10)
        ttk.Label(left_panel, text="Your favourite/saved books!", font=("Arial", 18, "italic"), anchor="center").pack(pady=0)

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

        
        if len(member["Wishlist"])>0:
            for isbn in member["Wishlist"]:
                book = read_book(isbn)
                book_frame = ttk.Frame(scrollable_frame, padding=10, style="default.TFrame")
                book_frame.pack(fill="x", pady=(0, 1))

                def on_hover(e, frame=book_frame):
                    frame.configure(style="hover.TFrame")

                def on_leave(e, frame=book_frame):
                    frame.configure(style="default.TFrame")

                book_frame.bind("<Enter>", on_hover)
                book_frame.bind("<Leave>", on_leave)

                
                wishlist_label = ttk.Label(
                    book_frame,
                    text=book["Title"],
                    font=("Helvetica", 14, "bold"),
                    foreground=ACCENT_COLOR,
                    anchor="w"
                )
                wishlist_label.pack(anchor="w", padx=5)
                wishlist_label.bind("<Button-1>", lambda e, isbn=book["ISBN"]: show_details_page(isbn))

                isbn_label = ttk.Label(
                    book_frame,
                    text=f"ISBN: {book['ISBN']}",
                    font=("Helvetica", 10),
                    anchor="w"
                )
                isbn_label.pack(anchor="w", padx=5)
                isbn_label.bind("<Button-1>", lambda e, isbn=book["ISBN"]: show_details_page(isbn))

                book_frame.bind("<Button-1>", lambda e, isbn=book["ISBN"]: show_details_page(isbn))
        else:
            ttk.Label(
                scrollable_frame,
                text="No book added to wishlist.",
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
            text="Detailed Information about this wishlisted book.",
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

        isbn = next((b for b in member["Wishlist"] if b == isbn), None)
        if not isbn:
            messagebox.showerror("Error", "Book not found.")
            show_main_page()
            return
        
        book = read_book(isbn)
        book_details = [
            ("Title", book["Title"]),
            ("ISBN", book["ISBN"]),
            ("Description", book["Description"]),
            ("Category", book["Category"]),
            ("Quantity", book["Quantity"]),
            ("Author", book["Author"]),
            ("Publisher", book["Publisher"]),
            ("Language", book["Language"]),
        ]

        for label, adetail in book_details:
            detail_frame = ttk.Frame(scrollable_frame, padding=10)
            detail_frame.pack(fill="x", pady=(0, 1))
                        
            detail = adetail

            if label == "Quantity":
                if int(detail) == 0:
                    detail = "All copies have been borrowed."
                else:
                    detail = f"{detail} copies in library."
           
            ttk.Label(
                detail_frame,
                text=f"{label}: {detail}",
                font=("Helvetica", 12),
                anchor="w",
                wraplength=350
            ).pack(anchor="w", padx=5)

        wishlist_button = ttk.Button(
            scrollable_frame,
            text="Remove from Wishlist",
            command=lambda:remove_from_wishlist(member["UID"], isbn),
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
