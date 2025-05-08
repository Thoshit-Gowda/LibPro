from mysql.connector import Error
from backend.sql import execQy, fOne
from backend.books import get_book_det

def add_book_inv(sku, isbn, status, bay, shelf, row, column):
    try:
        if not all([sku, isbn, status, bay, shelf, row, column]):
            return "All fields except BorrowedBy are required."

        if status not in ('Shelved', 'Unshelved', 'Missing', 'Damaged', 'Borrowed', 'Lost'):
            return "Invalid status."

        if not isbn.isdigit() or len(isbn) not in (10, 13):
            return "Invalid ISBN."

        book = get_book_det(isbn=isbn)
        if isinstance(book, str):
            return book 

        if not book:
            return "Book not found in catalog to derive category."

        category = book[0][5] 

        query = """
        INSERT INTO Inventory 
        (SKUNumber, ISBN, Status, Category, BayNumber, ShelfNumber, RowNumber, ColumnNumber)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (sku, isbn, status, category, bay, shelf, row, column)
        execQy(query, values)

        return "Inventory item added successfully."

    except Error as e:
        return f"Database error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

    
def update_book_inv(sku, status=None, borrowed_by=None, category=None,
                    bay=None, shelf=None, row=None, column=None):
    try:
        if not sku:
            return "SKU is required."

        if not fOne("SELECT * FROM Inventory WHERE SKUNumber = %s", (sku,)):
            return "SKU not found in inventory."

        updates = []
        values = []

        if status:
            allowed = ('Shelved', 'Unshelved', 'Missing', 'Damaged', 'Borrowed', 'Lost')
            if status not in allowed:
                return "Invalid status."
            updates.append("Status = %s")
            values.append(status)

        if borrowed_by is not None:
            updates.append("BorrowedBy = %s")
            values.append(borrowed_by)

        if category is not None:
            updates.append("Category = %s")
            values.append(category)

        if bay is not None:
            updates.append("BayNumber = %s")
            values.append(bay)

        if shelf is not None:
            updates.append("ShelfNumber = %s")
            values.append(shelf)

        if row is not None:
            updates.append("RowNumber = %s")
            values.append(row)

        if column is not None:
            updates.append("ColumnNumber = %s")
            values.append(column)

        if not updates:
            return "No fields provided to update."

        values.append(sku)  

        query = f"""
        UPDATE Inventory
        SET {', '.join(updates)}
        WHERE SKUNumber = %s
        """

        execQy(query, tuple(values))
        return "Inventory record updated successfully."

    except Error as e:
        return f"Database error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"
    
def get_book_inv(isbn=None, sku=None):
    try:
        query = "SELECT * FROM Inventory"
        values, conditions = [], []

        if isbn and isbn.isdigit() and len(isbn) in (10, 13):
            conditions.append("ISBN = %s")
            values.append(isbn.strip())
        elif isbn:
            return "Invalid ISBN."

        if sku:
            conditions.append("SKUNumber = %s")
            values.append(sku.strip())

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        rows = execQy(query, tuple(values))
        return rows or "No inventory records found."
    except Error as e:
        return f"Database error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

def delete_book_inv(sku=None, isbn=None, row=None, column=None, shelf=None, bay=None):
    try:
        conditions, values = [], []

        if sku:
            conditions.append("SKUNumber = %s")
            values.append(sku.strip())
        if isbn:
            if not isbn.isdigit() or len(isbn) not in (10, 13):
                return "Invalid ISBN."
            conditions.append("ISBN = %s")
            values.append(isbn.strip())
        if row:
            conditions.append("RowNumber = %s")
            values.append(row)
        if column:
            conditions.append("ColumnNumber = %s")
            values.append(column)
        if shelf:
            conditions.append("ShelfNumber = %s")
            values.append(shelf)
        if bay:
            conditions.append("BayNumber = %s")
            values.append(bay)

        if not conditions:
            return "At least one condition is required to delete inventory items."

        where_clause = " AND ".join(conditions)
        if not fOne(f"SELECT 1 FROM Inventory WHERE {where_clause}", tuple(values)):
            return "No matching inventory items found."

        execQy(f"DELETE FROM Inventory WHERE {where_clause}", tuple(values))
        return "Inventory item(s) deleted successfully."

    except Error as e:
        return f"Database error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

