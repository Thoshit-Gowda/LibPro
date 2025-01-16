import json
import os
import threading
import numpy
from tkinter import messagebox
import cv2
from pyzbar.pyzbar import decode

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

def clear_fields(*vars):
    for var in vars:
        var.set("")

def open_barcode_scanner(sku_var):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        messagebox.showerror("Error", "Could not access the webcam.")
        return

    line_position = 0
    line_direction = 1

    def stop_scanning():
        cap.release()
        cv2.destroyAllWindows()

    def scan_thread():
        nonlocal line_position, line_direction

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            barcodes = decode(frame)

            for barcode in barcodes:
                barcode_data = barcode.data.decode('utf-8').strip()
                sku_var.set(barcode_data)

                rect_points = barcode.polygon
                if len(rect_points) == 4:
                    pts = numpy.array(rect_points, dtype=numpy.int32)
                    cv2.polylines(frame, [pts], True, (0, 0, 255), 2)

                x, y, w, h = barcode.rect
                cv2.putText(frame, barcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                stop_scanning()
                return

            cv2.line(frame, (0, line_position), (frame.shape[1], line_position), (0, 255, 0), 2)
            line_position += line_direction
            if line_position >= frame.shape[0] or line_position <= 0:
                line_direction *= -1

            cv2.imshow("Barcode Scanner", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        stop_scanning()

    threading.Thread(target=scan_thread, daemon=True).start()
