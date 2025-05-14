import ttkbootstrap as ttk
from tkinter import messagebox
from ttkbootstrap.constants import *
from backend.account import get_user
from PIL import Image, ImageTk

from ui.content import dashboard_content
from ui.librarian.member_manager import member_manager
from ui.librarian.bay_manage import bay_manager
from ui.librarian.books_manage import books_manage
from ui.member.view_books import view_books

def open_dashboard(app, user,db):
    for widget in app.winfo_children():
        widget.destroy()
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return
    dashboard_content(app, user,db) 

def open_book_manager(app):
    for widget in app.winfo_children():
        widget.destroy()
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return
    books_manage(app)

def open_bay_manager(app):
    for widget in app.winfo_children():
        widget.destroy()
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return
    bay_manager(app)

def open_member_manager(app,admEmail):
    for widget in app.winfo_children():
        widget.destroy()
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return
    member_manager(app,admEmail)

def open_view_books(app, email):
    for widget in app.winfo_children():
        widget.destroy()
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return
    view_books(app, email)  

def logout(app):
    res = messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?")
    if res:
        from ui.login import login_screen
        for widget in app.winfo_children():
            widget.destroy()
        login_screen(app)

def dashboard(app, email, db):
    global welcome_frame
    if not app and db not in ["Librarian", "Members"]:
        messagebox.showerror("Error", "Application instance not found / database error.")
        return
    
    selected_button = {"current": None}

    def select_button(btn):
        if selected_button["current"]:
            selected_button["current"].configure(style="inactive.TButton")
        btn.configure(style="active.TButton")
        selected_button["current"] = btn

    userDet = get_user(db, email=email)

    image_path = "./ui/images/logo.png"
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

    if db == "Librarian":
        admin_dashboard_button =ttk.Button(menu_frame, text="Dashboard", command=lambda: [select_button(admin_dashboard_button),open_dashboard(main_frame, email,db)], style="inactive.TButton")
        admin_dashboard_button.pack(padx=5, fill="x", side="top", pady=(10,0))

        book_management_button = ttk.Button(menu_frame, text="View Books", command=lambda: [select_button(book_management_button),open_book_manager(main_frame)], style="inactive.TButton")
        book_management_button.pack(padx=5, fill="x", side="top")
        
        book_rack_management_button = ttk.Button(menu_frame, text="Bay Management", command=lambda: [select_button(book_rack_management_button),open_bay_manager(main_frame)], style="inactive.TButton")
        book_rack_management_button.pack(padx=5, fill="x", side="top")
    
        membership_management_button = ttk.Button(menu_frame, text="Membership Management", command=lambda: [select_button(membership_management_button),open_member_manager(main_frame,email)], style="inactive.TButton")
        membership_management_button.pack(padx=5, fill="x", side="top")

        select_button(admin_dashboard_button)
        
    elif db == "Members":
        admin_dashboard_button =ttk.Button(menu_frame, text="Dashboard", command=lambda: [select_button(admin_dashboard_button),open_dashboard(main_frame, email,db)], style="inactive.TButton")
        admin_dashboard_button.pack(padx=5, fill="x", side="top", pady=(10,0))

        book_management_button = ttk.Button(menu_frame, text="View Books", command=lambda: [select_button(book_management_button),open_view_books(main_frame, email)], style="inactive.TButton")
        book_management_button.pack(padx=5, fill="x", side="top")
        
        # book_rack_management_button = ttk.Button(menu_frame, text="Book Rack Management", command=lambda: [select_button(book_rack_management_button),open_rack_management(main_frame)], style="inactive.TButton")
        # book_rack_management_button.pack(padx=5, fill="x", side="top")
    
        # membership_management_button = ttk.Button(menu_frame, text="Membership Management", command=lambda: [select_button(membership_management_button),open_membership_management(main_frame)], style="inactive.TButton")
        # membership_management_button.pack(padx=5, fill="x", side="top")

        select_button(admin_dashboard_button)
    else: return("Invalid Input")  
    dashboard_content(main_frame, email, db)
    
    logout_button = ttk.Button(menu_frame, text="Logout", command=lambda: logout(app), style="crimson.TButton")
    logout_button.pack(padx=5, pady=50, fill="both", side="bottom")