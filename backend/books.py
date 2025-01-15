from datetime import datetime
from backend.utils import load_data, BOOKS_FILE

Books = []
Books = load_data(BOOKS_FILE)

def add_book(ISBN, Title, Description, Category, Quantity, Author, Publisher, Language, READD=False, SKU=None):
    if not ISBN or int(Quantity) <= 0:
        return "Invalid input for ISBN or Quantity."
    
    if READD:
        for book in Books:
            if book["ISBN"] == str(SKU).split("-")[0]:
                book["Quantity"] += 1
                date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                
                if not isinstance(book.get("SKU"), dict):
                    book["SKU"] = {}
                
                book["SKU"].setdefault(SKU, date)
                return "Book quantity updated successfully"

        # If book with ISBN not found, add it as a new book
        sku_dict = {SKU: datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        Books.append({
            "ISBN": str(SKU).split("-")[0],
            "Title": Title,
            "Description": Description,
            "Category": Category,
            "Quantity": 1,
            "SKU": sku_dict,
            "Author": Author,
            "Publisher": Publisher,
            "Language": Language,
        })
        return "Book re-added as a new entry"

    for book in Books:
        if book["ISBN"] == ISBN:
            for i in range(int(Quantity)):
                sku = f"{ISBN}-{len(book['SKU']) + i + 1}"
                date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                book["SKU"].setdefault(sku, date)
            book["Quantity"] += int(Quantity)
            return "Book quantity updated successfully"

    # Add new book
    sku_dict = {}
    for i in range(int(Quantity)):
        sku = f"{ISBN}-{i + 1}"
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        sku_dict[sku] = date

    Books.append({
        "ISBN": ISBN,
        "Title": Title,
        "Description": Description,
        "Category": Category,
        "Quantity": int(Quantity),
        "SKU": sku_dict,
        "Author": Author,
        "Publisher": Publisher,
        "Language": Language,
    })
    return "Book added successfully"

def update_books(ISBN, Title, Description, Category, Author, Publisher, Language):
    if not ISBN or not Title:
        return "Invalid input for ISBN or Title."

    for book in Books:
        if book["ISBN"] == ISBN:
            book["Title"] = Title
            book["Description"] = Description
            book["Category"] = Category
            book["Author"] = Author
            book["Publisher"] = Publisher
            book["Language"] = Language
            return "Book details updated successfully"
    return "No book found"

def remove_books(SKU, delete_all=False):
    if not SKU:
        return "Invalid SKU input."

    ISBN = (str(SKU).split("-")[0]).strip()
    sku = str(SKU).strip()

    for book in Books:
        if book["ISBN"] == ISBN:
            if delete_all:
                book["SKU"].clear()
                book["Quantity"] = 0
                return "All books with ISBN removed successfully"
            
            if sku in book["SKU"]:
                book["SKU"].pop(sku)
                if int(book["Quantity"]) > 0:
                    book["Quantity"] = int(book["Quantity"]) - 1
                    return "Book removed successfully"
                else:
                    return "Book quantity is already 0, cannot remove further"
            else:
                return f"SKU {sku} not found in the book"
    
    return f"Book with ISBN {ISBN} not found"

def read_book(ISBN):
    if not ISBN:
        return "Invalid ISBN input."

    for book in Books:
        if book["ISBN"] == ISBN:
            return book
    return "No book found"
