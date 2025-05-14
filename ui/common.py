import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def create_card(parent, title, value):
    frame = ttk.Frame(parent, padding=15, style="secondary.TFrame")
    frame.pack(side=LEFT, expand=True, fill=BOTH, padx=10)
    ttk.Label(frame, text=value, font=("Helvetica", 18, "bold")).pack()
    ttk.Label(frame, text=title, font=("Helvetica", 10)).pack()