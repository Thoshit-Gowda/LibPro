import ttkbootstrap as ttk
from tkinter import StringVar, messagebox
import re
from backend.members import add_member, remove_member, update_member, update_member_details

from backend.utils import open_barcode_scanner

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def open_add_member_popup(app, refresh_table_callback):
    popup = ttk.Toplevel(app)
    popup.geometry("600x400")
    popup.title("Add Member")
    popup.configure(bg="white")

    form_frame = ttk.Frame(popup)
    form_frame.pack(fill="both", expand=True)

    ttk.Label(form_frame, text="Add New Member", font=("Cambria", 18, "bold")).pack(pady=20)

    name_var = StringVar()
    email_var = StringVar()
    password_var = StringVar()

    fields = [
        ("Full Name", name_var),
        ("Email Address", email_var),
    ]

    for label, var in fields:
        ttk.Label(form_frame, text=label, font=("Century Gothic", 8)).pack(pady=5)
        ttk.Entry(form_frame, textvariable=var, font=("Century Gothic", 10)).pack(pady=5)

    ttk.Label(form_frame, text="Password", font=("Century Gothic", 8)).pack(pady=5)
    ttk.Entry(form_frame, textvariable=password_var, font=("Century Gothic", 10), show="*").pack(pady=5)
    
    def handle_add_member():
        name = name_var.get()
        email = email_var.get()
        password = password_var.get()

        if not is_valid_email(email):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        try:
            res = add_member(
                Name=name,
                Email=email,
                Password=password,
            )
            if "Error:" in res:
                messagebox.showerror("Error", res)
            else:
                messagebox.showinfo("Success", "Member added successfully!")
            refresh_table_callback()
            popup.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid data for Quantity.")

    ttk.Button(form_frame, text="Add Member", command=handle_add_member, style="crimson.TButton").pack(pady=10)

    ttk.Label(form_frame, text="Fill the details and click 'Add Member' to create new membership.", font=("Calibri", 10, "italic")).pack(pady=10)

def update_member_popup(app, member_data, refresh_table_callback):
    popup = ttk.Toplevel(app)
    popup.geometry("600x400")
    popup.title("Update Member Details")
    popup.configure(bg="white")

    form_frame = ttk.Frame(popup)
    form_frame.pack(fill="both", expand=True)

    ttk.Label(form_frame, text="Update Member Details", font=("Cambria", 18, "bold")).pack(pady=20)

    name_var = StringVar(value=member_data.get("Name", ""))
    old_password_var = StringVar()
    email_var = StringVar(value=member_data.get("Email", ""))
    new_password_var = StringVar()

    fields = [
        ("Full Name", name_var),
        ("Email Address", email_var),
    ]

    for label, var in fields:
        ttk.Label(form_frame, text=label, font=("Century Gothic", 8)).pack(pady=5)
        ttk.Entry(form_frame, textvariable=var, font=("Century Gothic", 10)).pack(pady=5)
    
    ttk.Label(form_frame, text="Old Password", font=("Century Gothic", 8)).pack(pady=5)
    ttk.Entry(form_frame, textvariable=old_password_var, font=("Century Gothic", 10), show="*").pack(pady=5)
    ttk.Label(form_frame, text="New Password", font=("Century Gothic", 8)).pack(pady=5)
    ttk.Entry(form_frame, textvariable=new_password_var, font=("Century Gothic", 10), show="*").pack(pady=5)

    def save_changes():
        updated_data = {label: var.get() for label, var in fields}
        updated_data["UID"] = member_data.get("UID", "")
        updated_data["New Password"] = new_password_var.get().strip()
        updated_data["Old Password"] = old_password_var.get().strip()

        if 'UID' not in updated_data or not updated_data["UID"]:
            messagebox.showerror("Error", "UID is required.")
            return

        if not is_valid_email(updated_data["Email Address"]):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        result = update_member_details(
            updated_data["UID"],
            updated_data["Full Name"],
            updated_data["Email Address"],
            updated_data["New Password"],
            updated_data["Old Password"],
        )
        if result == "Member details updated successfully":
            messagebox.showinfo("Success", result)
            refresh_table_callback()
            popup.destroy()
        elif result == "Old password is incorrect":
            messagebox.showerror("Error", "The old password you entered is incorrect. Please try again.")
        elif result == "No member found":
            messagebox.showerror("Error", "No member found with the given UID.")
        else:
            messagebox.showerror("Error", result+".")
        refresh_table_callback()
        popup.destroy()

    ttk.Button(form_frame, text="Save Changes", command=save_changes, style="crimson.TButton").pack(pady=10)

    ttk.Label(form_frame, text="Note: If you do not want to change the password, enter old password as new password.", font=("Calibri", 10, "italic")).pack(pady=10)
    ttk.Label(form_frame, text="Modify the details and click 'Save Changes' to update the member's details.", font=("Calibri", 10, "italic")).pack(pady=10)

def open_delete_member_popup(app, table, refresh_table_callback):
    selected_item = table.selection()
    if not selected_item:
        messagebox.showerror("Error", "No member selected!")
        return
    res = messagebox.askyesno("Confirm Deletion", "Are you sure you want to cancel membership?")
    if res:
        uid = table.item(selected_item)["values"][0]
        deletion_result = remove_member(uid)

        if deletion_result == "Member removed successfully":
            messagebox.showinfo("Success", "Membership cancelled successfully!")
            refresh_table_callback()
        else:
            messagebox.showerror("Error", deletion_result)


def open_update_member_book_popup(app, table, addbook, refresh_table_callback):
    selected_item = table.selection()
    if not selected_item:
        messagebox.showerror("Error", "No member selected!")
        return

    popup = ttk.Toplevel(app)
    popup.geometry("600x400")
    popup.title("Borrow or Return Book")
    popup.configure(bg="white")

    form_frame = ttk.Frame(popup)
    form_frame.pack(fill="both", expand=True)

    ttk.Label(form_frame, text="Borrow or Return Book", font=("Cambria", 18, "bold")).pack(pady=20)

    uid = table.item(selected_item)["values"][0]

    sku_var = StringVar()
    ttk.Label(form_frame, text="Enter SKU of Book", font=("Century Gothic", 10)).pack(pady=10)
    sku_entry = ttk.Entry(form_frame, textvariable=sku_var, font=("Century Gothic", 10))
    sku_entry.pack(pady=10)

    def handle_action():
        sku = sku_var.get()
        if not sku:
            messagebox.showerror("Error", "Please enter the SKU of the book!")
            return

        result = update_member(uid, sku, addbook)

        if "Fine incurred" in result:
            fine_confirmation = messagebox.askyesno(
                "Fine Confirmation", 
                f"{result}\n\nHas the fine been paid?"
            )
            if fine_confirmation:
                result = update_member(uid, sku, addbook, fine_paid=True)
                messagebox.showinfo("Success", result)
            else:
                messagebox.showinfo("Info", "The book will remain with member until the fine is paid.")
        
        elif "successfully" in result:
            messagebox.showinfo("Success", result)
        
        else:
            messagebox.showerror("Error", result)
        
        refresh_table_callback()
        popup.destroy()

    def start_scanning():
        open_barcode_scanner(sku_var) 

    ttk.Button(form_frame, text="Scan Barcode", command=start_scanning, style="crimson.TButton").pack(pady=5)
    ttk.Button(form_frame, text="Submit", command=handle_action, style="crimson.TButton").pack(pady=20)

    ttk.Label(form_frame, text="Fill in the SKU and click Submit to either borrow or return the book.", font=("Calibri", 10, "italic")).pack(pady=10)

    def on_close():
        popup.destroy()

    popup.protocol("WM_DELETE_WINDOW", on_close)
