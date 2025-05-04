from tkinter import ttk, messagebox
from ui.member_popups import open_add_member_popup, open_update_member_book_popup, update_member_popup, open_delete_member_popup
from backend.members import Members, read_member

def membership_manage(app):
    global table, table_frame

    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    table_frame = ttk.Frame(app)
    table_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    table_frame.grid_columnconfigure(0, weight=1)

    columns = ("UID", "Name", "Email", "Borrowed Books", "Join Date")
    table = ttk.Treeview(table_frame, columns=columns, show="headings", height=40)

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=100, anchor="center", stretch=True)

    scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=table.xview)
    table.configure(xscrollcommand=scrollbar.set)
    scrollbar.grid(row=1, column=0, sticky="ew")

    table.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

    button_frame = ttk.Frame(app)
    button_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
    button_frame.grid_columnconfigure(0, weight=1)

    ttk.Button(button_frame, text="Add New Member", command=lambda: open_add_member_popup(app, display_members), style="crimson.TButton").pack(fill="x", pady=5)
    ttk.Button(button_frame, text="Update Member Details", command=lambda: open_update_member_popup(app), style="crimson.TButton").pack(fill="x", pady=5)
    ttk.Button(button_frame, text="Delete Member", command=lambda: open_delete_member_popup(app, table, display_members), style="crimson.TButton").pack(fill="x", pady=5)
    ttk.Button(button_frame, text="Borrow Book", command=lambda: open_update_member_book_popup(app, table, True, display_members), style="crimson.TButton").pack(fill="x", pady=5)
    ttk.Button(button_frame, text="Return Book", command=lambda: open_update_member_book_popup(app, table, False, display_members), style="crimson.TButton").pack(fill="x", pady=5)

    app.grid_columnconfigure(0, weight=3)
    app.grid_columnconfigure(1, weight=1)

    display_members()

def open_update_member_popup(app):
    selected_item = table.selection()
    if not selected_item:
        messagebox.showerror("Error", "No member selected!")
        return

    UID = table.item(selected_item)["values"][0]
    if not UID:
        messagebox.showerror("Error", "Invalid UID!")
        return

    member = read_member(UID)

    if isinstance(member, str):
        messagebox.showerror("Error", "Member not found!")
        return

    update_member_popup(app, member, display_members)

def display_members():
    for row in table.get_children():
        table.delete(row)

    for index, member in enumerate(Members):
        table.insert("", "end", values=(
            member["UID"],
            member["Name"],
            member["Email"],
            member["SKU"],
            member["JoinedOn"],
        ))

def update_table(table):
    for row in table.get_children():
        table.delete(row)

    for member in Members:
        table.insert("", "end", values=(member["UID"], member["Name"], member["Email"], member["SKU"], member["JoinedOn"]))
