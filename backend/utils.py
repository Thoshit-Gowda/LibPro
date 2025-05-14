import time
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

def update_time(label):
    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%A, %B %d, %Y")
    label.config(text=f"{current_time}, {current_date}")
    label.after(1000, update_time, label)
