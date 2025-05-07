from datetime import datetime
import ttkbootstrap as ttk
from backend.books import read_book

ACCENT_COLOR = "#dc143c"

def view_borrowed_books(app, member):
    def go_to_dashboard():
        main_frame.pack_forget()
        #dashboard.welcome_screen(app, member)

    #for widget in app.winfo_children():
    #    widget.destroy()

    main_frame = ttk.Frame(app, padding=30)
    main_frame.pack(fill="both", expand=True)

    left_panel = ttk.Frame(main_frame, padding=20)
    left_panel.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    ttk.Label(left_panel, text="Borrowed Books", font=("Century Gothic", 40, "bold"), anchor="center").pack(pady=10)
    ttk.Label(left_panel, text="List of Books You have borrowed from the library.", font=("Arial", 18, "italic"), anchor="center").pack(pady=0)

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

    if len(member["SKU"]) > 0:
        for sku, duedate in member["SKU"].items():
            days_late = (datetime.now() - datetime.strptime(duedate, "%d/%m/%Y %H:%M:%S")).days
            day_text = "days late" if days_late > 0 else "days left"

            isbn = str(sku).split("-")[0].strip()
            book = read_book(isbn)

            book_frame = ttk.Frame(scrollable_frame, padding=10)
            book_frame.pack(fill="x", pady=(0, 1))

            def on_hover(e, frame=book_frame):
                frame.configure(style="hover.TFrame")

            def on_leave(e, frame=book_frame):
                frame.configure(style="default.TFrame")

            book_frame.bind("<Enter>", on_hover)
            book_frame.bind("<Leave>", on_leave)

            ttk.Label(
                book_frame,
                text=book["Title"],
                font=("Helvetica", 14, "bold"),
                foreground=ACCENT_COLOR,
            ).pack(anchor="w", padx=5)

            ttk.Label(
                book_frame,
                text=f"Status: {abs(days_late)} {day_text}",
                font=("Helvetica", 10),
            ).pack(anchor="w", padx=5)
    else:
        ttk.Label(
            scrollable_frame,
            text="No book borrowed.",
            font=("Helvetica", 14, "bold"),
        ).pack(anchor="w", padx=5)
