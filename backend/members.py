import math
import re
from backend.books import add_book, Books
from datetime import datetime, timedelta

from backend.utils import MEMBERS_FILE, load_data

Members = []
Members = load_data(MEMBERS_FILE)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def add_member(Name, Email, Password):
    if not Name.strip():
        return "Error: Name is required"
    if not Email.strip() or not is_valid_email(Email):
        return "Error: Valid email is required"
    if not Password.strip() or len(Password) < 6:
        return "Error: Password must be at least 6 characters"
    Members.append({
        "UID": len(Members) + 1,
        "Name": Name.strip(),
        "Email": Email.strip(),
        "Password": Password.strip(),
        "SKU": {},
        "Wishlist": [],
        "JoinedOn": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })
    return "Member added successfully"

def update_member_details(UID, NAME, EMAIL, PASSWORD, OLD_PASSWORD):
    if not UID or not str(UID).isdigit():
        return "Valid UID is required"
    if not NAME.strip():
        return "Name is required"
    if not EMAIL.strip() or not is_valid_email(EMAIL):
        return "Valid email is required"
    if not PASSWORD.strip() or len(PASSWORD) < 6:
        return "Password must be at least 6 characters"
    if not OLD_PASSWORD.strip():
        return "Old password is required"
    
    for member in Members:
        if str(member["UID"]) == str(UID):
            if str(member["Password"]) == str(OLD_PASSWORD):
                member["Name"] = NAME.strip()
                member["Email"] = EMAIL.strip()
                member["Password"] = PASSWORD.strip()
                return "Member details updated successfully"
            return "Old password is incorrect"
    return "No member found"

def update_member(UID, SKU, ADD_BOOK, fine_paid=False):
    if not UID or not str(UID).isdigit():
        return "Valid UID is required"
    if not SKU.strip():
        return "SKU is required"
    if ADD_BOOK not in [True, False]:
        return "ADD_BOOK must be either True or False"

    future_date = (datetime.now() + timedelta(days=15)).strftime("%d/%m/%Y %H:%M:%S")

    if ADD_BOOK:
        for book in Books:
            if str(book["ISBN"]) == str(SKU).split("-")[0]:
                if SKU in book["SKU"]:
                    for member in Members:
                        if member["UID"] == int(UID):
                            member["SKU"][SKU] = future_date
                            return "Book borrowed successfully"
        return "The book you are searching for is not available"
    else:
        for member in Members:
            if member["UID"] == int(UID):
                if SKU in member["SKU"]:
                    borrow_date = datetime.strptime(member["SKU"][SKU], "%d/%m/%Y %H:%M:%S")
                    days_late = (datetime.now() - borrow_date).days
                    
                    total_fine = 0
                    if days_late > 0:
                        fine = 5
                        for day in range(1, days_late + 1):
                            total_fine += math.ceil(fine)
                            fine += fine * 0.02

                        if not fine_paid:
                            return f"Days Late: {days_late}\nFine incurred: \u20B9{total_fine}/-."

                    member["SKU"].pop(SKU)
                    
                    res = add_book(
                        ISBN=str(SKU).split("-")[0],
                        Title="",
                        Description="",
                        Category="",
                        Quantity=1,
                        Author="",
                        Publisher="",
                        Language="",
                        READD=True,
                        SKU=SKU,
                    )
                    if res == "Invalid input for ISBN, Title, or Quantity.":
                        return "Error: Unable to add book to database."

                    if total_fine > 0 and fine_paid:
                        return f'Book returned successfully. Fine of \u20B9{total_fine}/- was paid.'
                    return "Book returned successfully. No fine incurred."

                return "Book not borrowed by this member"
        return "Member not found"

def remove_member(UID):
    if not UID or not str(UID).isdigit():
        return "Valid UID is required"
    for member in Members:
        if member["UID"] == int(UID):
            Members.remove(member)
            return "Member removed successfully"
    return "Member not found"

def sign_in(Email, Password):
    if not Email.strip() or not is_valid_email(Email):
        return "Valid email is required"
    if not Password.strip():
        return "Password is required"
    for member in Members:
        if member["Email"] == Email.strip() and member["Password"] == Password.strip():
            return member
    return "Invalid credentials"

def read_member(UID):
    if not UID or not str(UID).isdigit():
        return "Valid UID is required"
    for member in Members:
        if member["UID"] == int(UID):
            return member
    return "No member found"

def manage_wishlist(ADD, UID, ISBN):
    if not UID or not str(UID).isdigit() or not ISBN or ADD not in [True, False]:
        return "Valid parameters required"
    
    for mem in Members:
        if str(mem["UID"]) == str(UID):
            if ADD:
                if ISBN not in mem["Wishlist"]:
                    mem["Wishlist"].append(ISBN)
                else:
                    return "Error: Book already in wishlist"
            else:
                if ISBN in mem["Wishlist"]:
                    mem["Wishlist"].remove(ISBN)
                else:
                    return "Book not present in wishlist"
            return "Success"
    
    return "Error: UID is Invalid"
