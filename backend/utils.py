import json
import os

BOOKS_FILE = "./state/books_data.json"
MEMBERS_FILE = "./state/members_data.json"

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

def clear_fields(*vars):
    for var in vars:
        var.set("")