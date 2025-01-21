from datetime import datetime

from backend.utils import BOOK_SHELF_FILE, DESHELVED_BOOKS_FILE, load_data

BookShelf = []
DeshelvedBooks = {}

BookShelf = load_data(BOOK_SHELF_FILE)
DeshelvedBooks = load_data(DESHELVED_BOOKS_FILE)

def categorise(RACK, SHELF, CATEGORY):
    if not RACK or not SHELF or not CATEGORY:
        return "Error: Invalid input. RACK, SHELF, and CATEGORY are required."

    while len(BookShelf) < RACK:
        BookShelf.append([])

    while len(BookShelf[RACK - 1]) < SHELF:
        BookShelf[RACK - 1].append({})

    category_dict = BookShelf[RACK - 1][SHELF - 1]

    if CATEGORY not in category_dict:
        category_dict[CATEGORY] = []

    return f"Category '{CATEGORY}' added to rack {RACK}, shelf {SHELF}."

def shelf(RACK, SHELF, SKU):
    if not RACK or not SHELF or not SKU:
        return "Error: Invalid input. RACK, SHELF, and SKU are required."

    if RACK > len(BookShelf) or SHELF > len(BookShelf[RACK - 1]):
        return "Error: Rack or shelf does not exist."

    category_dict = BookShelf[RACK - 1][SHELF - 1]

    if not category_dict:
        return "Error: Shelf is uncategorized."

    for category in category_dict:
        if SKU not in category_dict[category]:
            category_dict[category].append(SKU)
            if SKU in DeshelvedBooks:
                DeshelvedBooks.pop(SKU)
            return f"Book with SKU '{SKU}' shelved successfully on rack {RACK}, shelf {SHELF} under category '{category}'."
    return "Error: SKU already exists in this category."

def search(SKU):
    if not SKU:
        return "Error: SKU is required for searching."

    for r, rack in enumerate(BookShelf, start=1):
        for s, shelf in enumerate(rack, start=1):
            if not shelf:
                continue

            for category, skus in shelf.items():
                if SKU in skus:
                    return f"Book with SKU '{SKU}' is located on rack {r}, shelf {s} under category '{category}'."
    return f"Error: Book with SKU '{SKU}' not found."


def deshelve(SKU):
    if not SKU:
        return "Error: SKU is required for deshelving."

    for r, rack in enumerate(BookShelf, start=1):
        for s, shelf in enumerate(rack, start=1):
            if not shelf:
                continue

            for category, skus in shelf.items():
                if SKU in skus:
                    skus.remove(SKU)
                    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    DeshelvedBooks[SKU] = f"Rack: {r}, Shelf: {s}, Timestamp: {timestamp}"
                    return f"Book with SKU '{SKU}' deshelved from rack {r}, shelf {s}."
    return f"Error: Book with SKU '{SKU}' not found."
