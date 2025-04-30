import time
from tkinter import messagebox, font
import ttkbootstrap as ttk
from PIL import Image, ImageTk

from ui.books_manage import books_manage
from ui.shelf_manage import shelf_manage
from ui.membership_manage import membership_manage
from ui.dashboard import admin_dashboard

from ui.client.view_books import view_books
from ui.client.view_borrowed_books import view_borrowed_books
from ui.client.wishlist import wishlist
from ui.client.dashboard import client_dashboard

ADMIN_CREDENTIALS = { # to check if everything is working fine.
    "Pratham": "123",
    "Thejas": "456",
    "Thoshit": "789",
}

def update_time(label):
    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%A, %B %d, %Y")
    label.config(text=f"Current Time: {current_time}\n{current_date}")
    label.after(1000, update_time, label)

def open_admin_dashboard(app, user):
    for widget in app.winfo_children():
        widget.destroy()
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return
    admin_dashboard(app, user)  

def open_client_dashboard(app, user):
    for widget in app.winfo_children():
        widget.destroy()
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return
    client_dashboard(app, user)      

def open_book_management(app):
    for widget in app.winfo_children():
        widget.destroy()
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return
    books_manage(app)    

def open_rack_management(app):
    for widget in app.winfo_children():
        widget.destroy()
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return
    shelf_manage(app)

def open_membership_management(app):
    for widget in app.winfo_children():
        widget.destroy()
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return
    membership_manage(app)

def open_view_books(app, member):
    for widget in app.winfo_children():
        widget.destroy()
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return
    view_books(app, member)   

def open_view_borrowed_books(app, member):
    for widget in app.winfo_children():
        widget.destroy()
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return
    view_borrowed_books(app, member)       

def open_wishlist(app, member):
    for widget in app.winfo_children():
        widget.destroy()
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return
    wishlist(app, member)  

def logout(app):
    res = messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?")
    if res:
        from ui.login_screen import login_screen
        for widget in app.winfo_children():
            widget.destroy()
        login_screen(app)

def welcome_screen(app, user):
    global welcome_frame
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return    

    image_path = "./library-management/backend/LibPro_logo.png"
    img = Image.open(image_path)
    img = img.resize((150, 55))
    photo = ImageTk.PhotoImage(img)

    welcome_frame = ttk.Frame(app)
    welcome_frame.pack(expand=True, fill="both")

    menu_frame = ttk.Frame(welcome_frame, style="My.TFrame")
    menu_frame.pack(fill="y", side="left")

    Img = ttk.Label(menu_frame, image=photo)
    Img.image = photo  
    Img.pack(pady=10)

    main_frame = ttk.Frame(welcome_frame)
    main_frame.pack(expand=True, fill="both")

    if user in ADMIN_CREDENTIALS:

        admin_dashboard_button =ttk.Button(menu_frame, text="Dashboard", command=lambda: open_admin_dashboard(main_frame, user), style="crimson.TButton")
        admin_dashboard_button.pack(padx=5, pady=10, fill="x", side="top")

        book_management_button = ttk.Button(menu_frame, text="menu_book", command=lambda: open_book_management(main_frame), style="crimson.TButton")
        book_management_button.pack(padx=5, pady=10, fill="x", side="top")
        
        book_rack_management_button = ttk.Button(menu_frame, text="Book Rack Management", command=lambda: open_rack_management(main_frame), style="crimson.TButton")
        book_rack_management_button.pack(padx=5, pady=10, fill="x", side="top")
    
        membership_management_button = ttk.Button(menu_frame, text="Membership Management", command=lambda: open_membership_management(main_frame), style="crimson.TButton")
        membership_management_button.pack(padx=5, pady=10, fill="x", side="top")

        admin_dashboard(main_frame, user)
    
    elif user not in ADMIN_CREDENTIALS:

        client_dashboard_button =ttk.Button(menu_frame, text="Dashboard", command=lambda: open_client_dashboard(main_frame, user), style="crimson.TButton")
        client_dashboard_button.pack(padx=5, pady=10, fill="x", side="top") 

        view_books_button = ttk.Button(menu_frame, text="View Books", command=lambda: open_view_books(main_frame, user), style="crimson.TButton")
        view_books_button.pack(padx=5, pady=10, fill="x", side="top")
    
        view_borrowed_books_button = ttk.Button(menu_frame, text="View Borrowed Books", command=lambda: open_view_borrowed_books(main_frame, user), style="crimson.TButton")
        view_borrowed_books_button.pack(padx=5, pady=10, fill="x", side="top")
    
        wishlist_button = ttk.Button(menu_frame, text="Wishlist", command=lambda: open_wishlist(main_frame, user), style="crimson.TButton")
        wishlist_button.pack(padx=5, pady=10, fill="x", side="top")

        client_dashboard(main_frame, user)

    else: return("Invalid Input")    

    logout_button = ttk.Button(menu_frame, text="Logout", command=lambda: logout(app), style="crimson.TButton")
    logout_button.pack(padx=5, pady=50, fill="both", side="bottom")

