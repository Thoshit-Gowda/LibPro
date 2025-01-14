import ttkbootstrap as ttk
from ui.login_screen import login_screen
from constants import APP_NAME

app = ttk.Window(themename="darkly")
app.geometry("1200x800") 
app.state('zoomed')
app.title(f"{APP_NAME} | Library Management App")
style = ttk.Style()
style.configure("crimson.TButton",
                background="#dc143c", 
                foreground="white",  
                borderwidth=0,
                focusthickness=0)

login_screen(app)
app.mainloop()
