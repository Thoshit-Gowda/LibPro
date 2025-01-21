from datetime import datetime
from backend.utils import load_data, BOOKS_FILE
import os
import shutil
from barcode import Code128
from barcode.writer import ImageWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


Books = load_data(BOOKS_FILE)

def is_valid_isbn(isbn):
    return len(isbn) == 10 or len(isbn) == 13 and isbn.isdigit()

def add_book(ISBN, Title, Description, Category, Quantity, Author, Publisher, Language, READD=False, SKU=None):
    if not ISBN or int(Quantity) <= 0 or not is_valid_isbn(ISBN):
        return "Invalid input for ISBN (must be 10 or 13 digits) or Quantity."
    
    if READD:
        for book in Books:
            if book["ISBN"] == str(SKU).split("-")[0]:
                book["Quantity"] += 1
                date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                
                if not isinstance(book.get("SKU"), dict):
                    book["SKU"] = {}
                
                book["SKU"].setdefault(SKU, date)
                return "Book quantity updated successfully"

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

def generate_barcodes_and_pdf(barcodes):
    output_dir = "barcodes"
    pdf_filename = "barcodes.pdf"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    barcode_images = []
    for barcode_data in barcodes:
        barcode = Code128(barcode_data, writer=ImageWriter())
        image_path = os.path.abspath(os.path.join(output_dir, f"{barcode_data}.png"))
        try:
            barcode.save(image_path[:-4])
            barcode_images.append(image_path)
        except Exception as e:
            return f"Error saving barcode {barcode_data}: {e}"

    if not barcode_images:
        return "No barcodes generated."

    try:
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        x, y = 50, 750

        for image in barcode_images:
            if not os.path.exists(image):
                continue
            try:
                c.drawImage(image, x, y, width=200, height=50)
                y -= 100
                if y < 100:
                    c.showPage()
                    y = 750
            except Exception as e:
                return f"Error adding image {image} to PDF: {e}"
        
        c.save()
    except Exception as e:
        return f"Error creating PDF: {e}"

    try:
        shutil.rmtree(output_dir)
    except Exception as e:
        return "PDF created but error deleting temporary folder."

    return f"Barcodes PDF saved as {os.path.abspath(pdf_filename)}"

def download_barcodes(book, save_path=None):
    if not book or "SKU" not in book:
        return "Error: Invalid book selected or no SKUs found."

    barcodes = list(book["SKU"].keys())
    if not barcodes:
        return "Error: No barcodes available for the selected book."

    pdf_result = generate_barcodes_and_pdf(barcodes)
    if pdf_result.startswith("Error"):
        return pdf_result

    if save_path:
        try:
            shutil.move("barcodes.pdf", save_path)
            return f"Success: Barcodes saved at {save_path}"
        except Exception as e:
            return f"Error saving file: {e}"

    return "Success: Barcodes PDF generated but not saved."

def update_books(ISBN, Title, Description, Category, Author, Publisher, Language):
    if not ISBN or not Title or not is_valid_isbn(ISBN):
        return "Invalid input for ISBN (must be 10 or 13 digits) or Title."

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
                    return "Error: Book quantity is already 0, cannot remove further"
            else:
                return f"Error: SKU {sku} not found in the database"
    
    return f"Error Book with ISBN {ISBN} not found"

def read_book(ISBN):
    if not ISBN or not is_valid_isbn(ISBN):
        return "Invalid ISBN input (must be 10 or 13 digits)."

    for book in Books:
        if book["ISBN"] == ISBN:
            return book
    return "No book found"
