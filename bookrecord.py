from mysql.connector import Error
from backend.account import add_points_mem
from backend.inventory import update_book_inv
from backend.sql import execQy, fAll, fOne
from datetime import datetime, timedelta

def borrow_book(email, sku, fullname, isbn, daysborrowed):
    try:
        if not email or not sku or not fullname or not isbn or daysborrowed is None:
            return "All fields are required."

        email = str(email).strip()
        sku = str(sku).strip()
        fullname = str(fullname).strip()
        isbn = str(isbn).strip()
        days = str(daysborrowed).strip()

        if not days.isdigit() or int(days) <= 0:
            return "Days borrowed must be a positive integer."
        days = int(days)

        if fOne("SELECT * FROM BooksRecord WHERE SKU = %s AND Status = 'Borrowed'", (sku,)):
            return "This book is already borrowed and not yet returned."

        if not fOne("SELECT * FROM Books WHERE ISBN = %s", (isbn,)):
            return "Invalid ISBN: Book not found."

        due_on = (datetime.now() + timedelta(days=days)).date()

        query = """
        INSERT INTO BooksRecord 
        (SKU, Status, ISBN, Email, FullName, DaysBorrowed, DueOn)
        VALUES (%s, 'Borrowed', %s, %s, %s, %s, %s)
        """
        values = (sku, isbn, email, fullname, days, due_on)
        execQy(query, values)
        update_book_inv(sku, status="Borrowed", borrowed_by=email)

        return "Book borrowed successfully."

    except Error as e:
        return f"Database error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


def return_book(sku):
    try:
        if not sku:
            return "SKU is required."

        record = fOne("SELECT Status, DueOn, Email, ISBN FROM BooksRecord WHERE SKU = %s", (sku,))
        if not record:
            return "Book record not found."

        status, due_on, email, isbn = record

        if status != "Borrowed":
            return "Book is not currently marked as borrowed."

        today = datetime.now().date()
        days_late = max((today - due_on).days, 0)
        fine = round(days_late * 2.0, 2)
        points = 0

        if days_late == 0:
            points = add_points_mem(email, isbn, 1) or 0 

        query = """
        UPDATE BooksRecord
        SET Status = 'Returned',
            ReturnedOn = %s,
            DaysLate = %s,
            Fine = %s,
            Points = %s
        WHERE SKU = %s
        """
        values = (today, days_late, fine, points, sku)
        execQy(query, values)
        update_book_inv(sku, status="Unshelved", borrowed_by=None)

        return f"Book returned successfully.\n\nFine to be paid: ₹{fine:.2f}/-\nPoints awarded: {points}."

    except Error as e:
        return f"Database error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

def get_record(sku=None):
    try:
        if not sku:
            rec = fAll("SELECT * FROM BooksRecord")
            if not rec:
                return "No records found."
            return rec

        record = fOne("""
            SELECT SKU, Status, ISBN, Email, FullName, DaysBorrowed, DueOn,
                   ReturnedOn, DaysLate, Fine, Points, CreatedOn, UpdatedOn
            FROM BooksRecord
            WHERE SKU = %s
        """, (sku,))

        if not record:
            return "No record found for the given SKU."

        fields = ["SKU", "Status", "ISBN", "Email", "FullName", "DaysBorrowed", "DueOn",
                  "ReturnedOn", "DaysLate", "Fine", "Points", "CreatedOn", "UpdatedOn"]

        result = {field: value for field, value in zip(fields, record)}

        result["Fine"] = f"₹{result['Fine']:.2f}/-" if result["Fine"] else "₹0.00/-"
        result["Points"] = result["Points"] or 0
        result["ReturnedOn"] = result["ReturnedOn"] or "Not yet returned"
        result["DaysLate"] = result["DaysLate"] or 0

        return result

    except Error as e:
        return f"Database error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"
