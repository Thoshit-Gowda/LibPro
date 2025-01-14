import time
from tkinter import messagebox
import ttkbootstrap as ttk

from ui.membership_manage import membership_manage
from ui.books_manage import books_manage

def update_time(label):
    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%A, %B %d, %Y")
    label.config(text=f"Current Time: {current_time}\n{current_date}")
    label.after(1000, update_time, label)

def open_book_management(app):
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return
    welcome_frame.pack_forget()
    books_manage(app)

def logout(app):
    res = messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?")
    if res:
        from ui.login_screen import login_screen
        welcome_frame.pack_forget()
        login_screen(app)

def open_membership_management(app):
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return
    welcome_frame.pack_forget()
    membership_manage(app)

def welcome_screen(app):
    global welcome_frame
    if not app:
        messagebox.showerror("Error", "Application instance not found.")
        return
    welcome_frame = ttk.Frame(app, padding=30)
    welcome_frame.pack(expand=True, fill="both", pady=100)

    form_frame = ttk.Frame(welcome_frame)
    form_frame.pack(fill="both", expand=True)

    left_frame = ttk.Frame(form_frame, padding=20)
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    
    ttk.Label(left_frame, text="LibAmma", font=("Century Gothic", 40, "bold"), anchor="center").pack(pady=10)
    ttk.Label(left_frame, text="Library Management App", font=("Arial", 18, "italic"), anchor="center").pack(pady=0)

    time_label = ttk.Label(left_frame, font=("Arial", 12))
    time_label.pack(pady=10)
    update_time(time_label)

    greeting_label = ttk.Label(left_frame, text="Welcome Admin!", font=("Arial", 10, "bold"))
    greeting_label.pack(pady=10)

    right_frame = ttk.Frame(form_frame, padding=20)
    right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    book_management_button = ttk.Button(right_frame, text="Books Management", command=lambda: open_book_management(app), style="crimson.TButton")
    book_management_button.pack(pady=10, fill="x")

    membership_management_button = ttk.Button(right_frame, text="Membership Management", command=lambda: open_membership_management(app), style="crimson.TButton")
    membership_management_button.pack(pady=10, fill="x")

    logout_button = ttk.Button(right_frame, text="Logout", command=lambda: logout(app), style="crimson.TButton")
    logout_button.pack(pady=50, fill="both")

    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=1)
    form_frame.grid_rowconfigure(0, weight=1)
