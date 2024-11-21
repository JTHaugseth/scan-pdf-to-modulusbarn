import os
import base64
import time
import shutil
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from token_handler import get_access_token

# Modulus-barn API-url
API_URL = "PASTE_MODULUS-BARN_API_URL_HERE"

# Folder paths for logging, input, and processed files
LOG_FOLDER = "log"
LOG_FILE = os.path.join(LOG_FOLDER, "log.txt")
SCAN_ENTRY_FOLDER = "scan-entry"
SCAN_FAILED_FOLDER = "scan-failed"
SCAN_FINISHED_FOLDER = "scan-finished"

# Ensure all required directories exist
def ensure_directories_exist():
    os.makedirs(LOG_FOLDER, exist_ok=True)
    os.makedirs(SCAN_ENTRY_FOLDER, exist_ok=True)
    os.makedirs(SCAN_FAILED_FOLDER, exist_ok=True)
    os.makedirs(SCAN_FINISHED_FOLDER, exist_ok=True)

# Move file to a specified destination folder
def move_file(file_path, destination_folder):
    try:
        destination_path = os.path.join(destination_folder, os.path.basename(file_path))
        shutil.move(file_path, destination_path)
        print(f"Moved {file_path} to {destination_folder}")
    except Exception as e:
        print(f"Failed to move {file_path} to {destination_folder}: {e}")

# Log successful upload to the log file
def log_success(title):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"Successfully uploaded {title} at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

# Convert PDF file to a base64-encoded string
def get_base64_encoded_pdf(file_path):
    with open(file_path, "rb") as pdf_file:
        return base64.b64encode(pdf_file.read()).decode("utf-8")

# Send PDF file to the API, handling success and failure cases
def send_to_api(encoded_content, title, file_path):
    try:
        token = get_access_token()
    except Exception as e:
        print(f"Failed to obtain token: {e}")
        move_file(file_path, SCAN_FAILED_FOLDER)
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "title": title,
        "documents": [
            {
                "title": title,
                "File": encoded_content,
                "MimeType": "application/pdf"
            }
        ]
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        print("Response Status:", response.status_code)

        if response.status_code in [200, 204]:
            print(f"Sent {title} successfully.")
            log_success(title)
            move_file(file_path, SCAN_FINISHED_FOLDER)
        else:
            print(f"Failed to send {title}: {response.status_code} {response.text}")
            move_file(file_path, SCAN_FAILED_FOLDER)
    except Exception as e:
        print(f"Error during API request: {e}")
        move_file(file_path, SCAN_FAILED_FOLDER)

# Check if the file is ready for processing (not locked or incomplete) 
def is_file_ready(filepath):
    time.sleep(1) # Allow time for file operations to complete before we process it
    try:
        with open(filepath, 'rb'):
            return True
    except IOError:
        return False

# Event handler for monitoring the scan-entry folder for new files
class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(".pdf"):
            return
        print(f"Detected new PDF: {event.src_path}")
        
        if is_file_ready(event.src_path): # Process the file if it's ready
            base64_content = get_base64_encoded_pdf(event.src_path)
            send_to_api(base64_content, title=os.path.basename(event.src_path), file_path=event.src_path)
        else: # Move to failed folder if file isn't ready
            print(f"File not ready: {event.src_path}")
            move_file(event.src_path, SCAN_FAILED_FOLDER)

# Main script execution
if __name__ == "__main__":
    ensure_directories_exist()
    event_handler = PDFHandler()
    observer = Observer() # Create an observer to monitor the folder
    observer.schedule(event_handler, SCAN_ENTRY_FOLDER, recursive=False) # Monitor scan-entry folder
    observer.start()
    print(f"Monitoring folder: {SCAN_ENTRY_FOLDER}")
    try:
        while True:
            time.sleep(1) 
    except KeyboardInterrupt:
        observer.stop()
    observer.join()