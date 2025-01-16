import ttkbootstrap as ttk
from tkinter import messagebox
import tkinter as tk

from backend.members import sign_in
from ui.client.dashboard import welcome_screen

def login_screen(app):
    global login_frame, email_var, password_var

    login_frame = ttk.Frame(app, padding=30)
    login_frame.pack(expand=True, fill="both")

    branding_frame = ttk.Frame(login_frame, padding=20)
    branding_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
    
    ttk.Label(branding_frame, anchor="center").pack(pady=70)

    ttk.Label(branding_frame, text="LibAmma", font=("Century Gothic", 40, "bold"), anchor="center").pack(pady=10)

    ttk.Label(branding_frame, text="A Library App.", font=("Arial", 18, "italic"), anchor="center").pack(pady=0)

    ttk.Label(branding_frame, text="By Pratham, Thejas and Thoshit.", font=("Arial", 12), anchor="center").pack(pady=50)

    login_section = ttk.Frame(login_frame, padding=20)
    login_section.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    canvas = tk.Canvas(login_section, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    width = 500
    height = 500
    radius = 20
    canvas.create_oval(0, 0, radius * 2, radius * 2, outline="#ffffff")
    canvas.create_rectangle(radius, 0, width - radius, height, outline="#ffffff")
    canvas.create_oval(width - radius * 2, 0, width, radius * 2, outline="#ffffff")
    canvas.create_rectangle(0, radius, width, height - radius, outline="#ffffff")
    canvas.create_oval(0, height - radius * 2, radius * 2, height, outline="#ffffff")
    canvas.create_oval(width - radius * 2, height - radius * 2, width, height, outline="#ffffff")

    form_frame = ttk.Frame(canvas)
    canvas.create_window(width // 2, height // 2, window=form_frame, anchor="center")

    ttk.Label(form_frame, text="Member Login", font=("Cambria", 30, "bold")).pack(pady=20)

    ttk.Label(form_frame, text="Email Address:", font=("Century Gothic", 14)).pack(anchor="w", pady=5)
    email_var = ttk.StringVar()
    ttk.Entry(form_frame, textvariable=email_var, font=("Century Gothic", 12)).pack(fill="x", pady=5)

    ttk.Label(form_frame, text="Password:", font=("Century Gothic", 14)).pack(anchor="w", pady=5)
    password_var = ttk.StringVar()
    ttk.Entry(form_frame, textvariable=password_var, font=("Century Gothic", 12), show="*").pack(fill="x", pady=5)

    ttk.Button(form_frame, text="Login", command=lambda: validate_login(app), style="crimson.TButton").pack(pady=20, fill="x")

    ttk.Label(form_frame, text="Welcome to the modern library experience.", font=("Calibri", 10, "italic")).pack(side="bottom", pady=10)


def validate_login(app):
    email = email_var.get().strip()
    password = password_var.get().strip()

    if not email or not password:
        messagebox.showerror("Error", "Email and password cannot be empty.")
        return
    res = sign_in(email, password)
    if res == "Invalid credentials" or res == "Valid email is required" or res == "Password is required":
        messagebox.showerror("Error", res)
    else:
        messagebox.showinfo("Success", "Login successful!")
        login_frame.pack_forget()
        welcome_screen(app, res)
