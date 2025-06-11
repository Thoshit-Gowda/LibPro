import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Frame, Label, Treeview, Scrollbar
from backend.bookrecord import get_record 
from backend.books import get_book_det

redemption_items = [
        {"name": "Library Tote Bag", "cost": 100},
        {"name": "Notebook", "cost": 80},
        {"name": "Pen Set", "cost": 50},
        {"name": "Free Book", "cost": 200}
    ]

def points_dashboard(app, email):
    
        userDet = get_record(email= email)[0]
        print(userDet)
        bookDet = get_book_det(isbn= userDet[2])

        # USER INFO CARD
        user_frame = Frame(app, padding=15, bootstyle="dark")
        user_frame.pack(fill="x", pady=10)

        Label(user_frame, text=f"👤 User: {userDet[4]}", font=("Segoe UI", 14, "bold"), bootstyle="light").pack(anchor="w")
        Label(user_frame, text=f"📚 Books Borrowed: {bookDet}", font=("Segoe UI", 12), bootstyle="light").pack(anchor="w")
        Label(user_frame, text=f"⭐ Points: {userDet[7]}", font=("Segoe UI", 12), bootstyle="success").pack(anchor="w")

        # REDEMPTION LIST SECTION
        redeem_label = Label(user_frame, text="🎁 Redemption Items", font=("Segoe UI", 14, "bold"))
        redeem_label.pack(anchor="w", pady=(20, 5))

        columns = ("Item", "Points Required")
        tree = Treeview(user_frame, columns=columns, show="headings", bootstyle="info")
        tree.heading("Item", text="Item")
        tree.heading("Points Required", text="Points Required")
        tree.column("Item", width=200,anchor="center")
        tree.column("Points Required", width=150, anchor="center")
        tree.pack(fill="both", expand=True)

        for item in redemption_items:
            tree.insert("", "end", values=(item["name"], item["cost"]))

        # Scrollbar
        scrollbar = Scrollbar(user_frame, orient="vertical", command=tree.yview, bootstyle="dark-round")
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(relx=1.0, rely=0, relheight=1.0, anchor='ne')
    