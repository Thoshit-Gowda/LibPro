from tkinter import messagebox
import ttkbootstrap as ttk
from backend.utils import BOOKS_FILE, MEMBERS_FILE, BOOK_SHELF_FILE, DESHELVED_BOOKS_FILE, save_data
from ui.login_screen import login_screen
from constants import APP_NAME
from backend.books import Books
from backend.members import Members
from backend.shelfing import BookShelf, DeshelvedBooks

def on_close():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        print("App is closing. Saving data...")
        save_data(Books, BOOKS_FILE)
        save_data(Members, MEMBERS_FILE)
        save_data(BookShelf, BOOK_SHELF_FILE)
        save_data(DeshelvedBooks, DESHELVED_BOOKS_FILE)
        app.destroy()

app = ttk.Window(themename="darkly")
app.geometry("1200x800") 
app.state('zoomed')
app.title(f"{APP_NAME} | Library Management App")

app.protocol("WM_DELETE_WINDOW", on_close)

style = ttk.Style()
style.configure("crimson.TButton",
                background="#4682B4", 
                foreground="White",  
                borderwidth=0,
                focusthickness=0)
            
style.configure("inactive.TButton",
                background="#171717", 
                foreground="white",  
                borderwidth=0,
                focusthickness=0,
                padding=20)

style.configure("active.TButton",
                background="#4682B4",
                foreground="white",
                relief="flat",
                borderwidth=0,
                padding=20) 

style.configure("My.TFrame", background="#171717")

style.configure("secondary.TFrame", background="#4682B4")

login_screen(app)
app.mainloop()