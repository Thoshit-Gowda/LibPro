import ttkbootstrap as ttk
from tkinter import messagebox
import tkinter as tk
from ui.main_screen import welcome_screen
from backend.members import sign_in
from PIL import Image, ImageTk


ADMIN_CREDENTIALS = {
    "Pratham": "123",
    "Thejas": "456",
    "Thoshit": "789",
}

def login_screen(app):
    global login_frame, username_var, password_var

    login_frame = ttk.Frame(app, padding=30)
    login_frame.pack(expand=True, fill="both")

    branding_frame = ttk.Frame(login_frame, padding=20)
    branding_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    image_path = "./backend/Branding_image.png"
    img = Image.open(image_path)
    img = img.resize((450, 450))
    photo = ImageTk.PhotoImage(img)

    Img1 = tk.Label(branding_frame, image=photo, bg="#1e1e1e")
    Img1.image = photo  
    Img1.place(relx=0.5, rely=0.5, anchor="center")
    Img1.pack(expand=True, pady=40)
    
    ttk.Label(branding_frame, anchor="center").pack(pady=70)

    login_section = ttk.Frame(login_frame, padding=20)
    login_section.pack(side="right", fill="both", expand=True, padx=10, pady=20)

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

    ttk.Label(form_frame, text="Login", font=("Gotham Bold", 40, "bold")).pack(pady=20)

    ttk.Label(form_frame, text="Username:", font=("Century Gothic", 14)).pack(anchor="w", pady=5)
    username_var = ttk.StringVar()
    ttk.Entry(form_frame, textvariable=username_var, font=("Century Gothic", 12)).pack(fill="x", pady=5)

    ttk.Label(form_frame, text="Password:", font=("Century Gothic", 14)).pack(anchor="w", pady=5)
    password_var = ttk.StringVar()
    ttk.Entry(form_frame, textvariable=password_var, font=("Century Gothic", 12), show="*").pack(fill="x", pady=5)

    ttk.Button(form_frame, text="Login", command=lambda: validate_login(app), style="crimson.TButton").pack(pady=20, fill="x")

    ttk.Label(form_frame, text="Welcome to the modern library experience.", font=("Calibri", 10, "italic")).pack(side="bottom", pady=10)


def validate_login(app):
    username = username_var.get().strip()
    password = password_var.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty.")
        return

    if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
        messagebox.showinfo("Success", "Login successful!")
        login_frame.pack_forget()
        welcome_screen(app, username)  #Thought of adding a argument for the data of the user or the admin.

    elif sign_in(username, password):
        messagebox.showinfo("Success", "Login successful!")
        login_frame.pack_forget()
        welcome_screen(app, username)
        
    else:
        messagebox.showerror("Error", "Invalid username or password.")
