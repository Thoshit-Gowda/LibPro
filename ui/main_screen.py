import time
from tkinter import messagebox, font
import ttkbootstrap as ttk
from PIL import Image, ImageTk

from ui.books_manage import books_manage
from ui.shelf_manage import shelf_manage
from ui.membership_manage import membership_manage
from ui.dashboard import dashboard

from ui.client.view_books import view_books
from ui.client.view_borrowed_books import view_borrowed_books
from ui.client.wishlist import wishlist
from backend.utils import load_data, MEMBERS_FILE

Members = load_data(MEMBERS_FILE)

ADMIN_CREDENTIALS =[{
   "Name": "Pratham",
   "Password": "123"
   },{
    "Name": "Thejas",
    "Password": "456"
   },{
    "Name": "Thoshit",
    "Password": "789"
   }]

def update_time(label):
    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%A, %B %d, %Y")
    label.config(text=f"Current Time: {current_time}\n{current_date}")
    label.after(1000, update_time, label)

def open_dashboard(app, user):
    for widget in app.winfo_children():
        widget.destroy()
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return
    dashboard(app, user)     

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

    selected_button = {"current": None}

    def select_button(btn):
        # Reset the previously selected button's style
        if selected_button["current"]:
            selected_button["current"].configure(style="inactive.TButton")
        # Set the new button's style
        btn.configure(style="active.TButton")
        selected_button["current"] = btn

    image_path = "./backend/Images/LibPro_logo.png"
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

    if user in ADMIN_CREDENTIALS and user not in Members:

        admin_dashboard_button =ttk.Button(menu_frame, text="Dashboard", command=lambda: [select_button(admin_dashboard_button),open_dashboard(main_frame, user)], style="inactive.TButton")
        admin_dashboard_button.pack(padx=5, fill="x", side="top", pady=(10,0))

        book_management_button = ttk.Button(menu_frame, text="View Books", command=lambda: [select_button(book_management_button),open_book_management(main_frame)], style="inactive.TButton")
        book_management_button.pack(padx=5, fill="x", side="top")
        
        book_rack_management_button = ttk.Button(menu_frame, text="Book Rack Management", command=lambda: [select_button(book_rack_management_button),open_rack_management(main_frame)], style="inactive.TButton")
        book_rack_management_button.pack(padx=5, fill="x", side="top")
    
        membership_management_button = ttk.Button(menu_frame, text="Membership Management", command=lambda: [select_button(membership_management_button),open_membership_management(main_frame)], style="inactive.TButton")
        membership_management_button.pack(padx=5, fill="x", side="top")

        dashboard(main_frame, user)
        select_button(admin_dashboard_button)
    
    elif user not in ADMIN_CREDENTIALS and user in Members:

        client_dashboard_button =ttk.Button(menu_frame, text="Dashboard", command=lambda: [select_button(client_dashboard_button),open_dashboard(main_frame, user)], style="inactive.TButton")
        client_dashboard_button.pack(padx=5, pady=(10,0), fill="x", side="top") 

        view_books_button = ttk.Button(menu_frame, text="View Books", command=lambda: [select_button(view_books_button),open_view_books(main_frame, user)], style="inactive.TButton")
        view_books_button.pack(padx=5, fill="x", side="top")
    
        view_borrowed_books_button = ttk.Button(menu_frame, text="View Borrowed Books", command=lambda: [select_button(view_borrowed_books_button),open_view_borrowed_books(main_frame, user)], style="inactive.TButton")
        view_borrowed_books_button.pack(padx=5, fill="x", side="top")
    
        wishlist_button = ttk.Button(menu_frame, text="Wishlist", command=lambda: [select_button(wishlist_button),open_wishlist(main_frame, user)], style="inactive.TButton")
        wishlist_button.pack(padx=5,  fill="x", side="top")

        dashboard(main_frame, user)
        select_button(client_dashboard_button)

    else: return("Invalid Input")    

    logout_button = ttk.Button(menu_frame, text="Logout", command=lambda: logout(app), style="crimson.TButton")
    logout_button.pack(padx=5, pady=50, fill="both", side="bottom")

