import re
from backend.books import remove_books, add_book, Books
from datetime import datetime, timedelta

Members = []

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def add_member(Name, Email, Password):
    if not Name.strip():
        return "Name is required"
    if not Email.strip() or not is_valid_email(Email):
        return "Valid email is required"
    if not Password.strip() or len(Password) < 6:
        return "Password must be at least 6 characters"
    Members.append({
        "UID": len(Members) + 1,
        "Name": Name.strip(),
        "Email": Email.strip(),
        "Password": Password.strip(),
        "SKU": {},
        "JoinedOn": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })
    return "Member added successfully"

def update_member_details(UID, NAME, EMAIL, PASSWORD, OLD_PASSWORD):
    if not UID or not UID.isdigit():
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
            if member["Password"] == OLD_PASSWORD:
                member["Name"] = NAME.strip()
                member["Email"] = EMAIL.strip()
                member["Password"] = PASSWORD.strip()
                return "Member details updated successfully"
            return "Old password is incorrect"
    return "No member found"

def update_member(UID, SKU, ADD_BOOK):
    if not UID or not UID.isdigit():
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
                            remove_books(SKU)
                            return "Book borrowed successfully"
        return "The book you are searching for is not available"
    else:
        for member in Members:
            if member["UID"] == int(UID):
                if SKU in member["SKU"]:
                    borrow_date = datetime.strptime(member["SKU"][SKU], "%d/%m/%Y %H:%M:%S")
                    member["SKU"].pop(SKU)
                    add_book("", "", "", "", 1, "", "", "", True, SKU)
                    days_late = (datetime.now() - borrow_date).days - 15
                    if days_late > 0:
                        fine = 5
                        total_fine = 0
                        for day in range(1, days_late + 1):
                            total_fine += fine
                            fine += fine * 0.02
                        return f"Book returned successfully. Fine incurred: {total_fine:.2f}"
                    return "Book returned successfully. No fine incurred"
                return "Book not borrowed by this member"
        return "Member not found"

def remove_member(UID):
    if not UID or not UID.isdigit():
        return "Valid UID is required"
    for member in Members:
        if member["UID"] == int(UID):
            Members.remove(member)
            return "Member removed successfully"
    return "Member not found"

def sign_in(Name, Email, Password):
    if not Name.strip():
        return "Name is required"
    if not Email.strip() or not is_valid_email(Email):
        return "Valid email is required"
    if not Password.strip():
        return "Password is required"
    for member in Members:
        if member["Name"] == Name.strip() and member["Email"] == Email.strip() and member["Password"] == Password.strip():
            return member
    return "Invalid credentials"

def read_member(UID):
    if not UID or not UID.isdigit():
        return "Valid UID is required"
    for member in Members:
        if member["UID"] == int(UID):
            return member
    return "No member found"
