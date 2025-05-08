import os
import json
import base64
from backend.constants import ENCRYPTION_KEY

def validate_fields(fields, valid_fields):
    if not fields:
        return "*"
    
    valid_fields = []
    for f in fields:
        if f in valid_fields:
            valid_fields.append(f)
    
    if not valid_fields:
        return "INVALID" 
    
    return ", ".join(valid_fields)

def encrypt_password(password):
    encrypted = ''.join(chr(ord(c) ^ ord(ENCRYPTION_KEY[i % len(ENCRYPTION_KEY)])) for i, c in enumerate(password))
    return base64.b64encode(encrypted.encode()).decode()

def decrypt_password(encoded):
    decoded = base64.b64decode(encoded.encode()).decode()
    return ''.join(chr(ord(c) ^ ord(ENCRYPTION_KEY[i % len(ENCRYPTION_KEY)])) for i, c in enumerate(decoded))



BOOKS_FILE = "./state/books_data.json"
MEMBERS_FILE = "./state/members_data.json"
BOOK_SHELF_FILE = "./state/book_shelf_data.json"
DESHELVED_BOOKS_FILE = "./state/deshelved_books_data.json"

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_data(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
