from tkinter import messagebox
import ttkbootstrap as ttk
from admin.login_screen import login_screen

def on_close():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        app.destroy()

app = ttk.Window(themename="darkly")
app.geometry("1200x800") 
app.state('zoomed')
app.title("LibPro | Library Management App")

app.protocol("WM_DELETE_WINDOW", on_close)

style = ttk.Style()
style.configure("crimson.TButton",
                background="#dc143c", 
                foreground="white",  
                borderwidth=0,
                focusthickness=0)

login_screen(app)
app.mainloop()