import os
import tkinter as tk
from tkinter import filedialog
from google.cloud import storage

# Set the path to your JSON authentication file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./ec530-final-project-384115-9b7b441d7031.json"

# Replace with your Google Cloud Storage bucket name
BUCKET_NAME = "bucket-quickstart_ec530-final-project-384115"

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_label.config(text=file_path)
        upload_file_to_gcs(file_path)

def upload_file_to_gcs(file_path):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    file_name = os.path.basename(file_path)
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_path)
    print(f"File {file_path} uploaded to {BUCKET_NAME} as {file_name}.")

root = tk.Tk()
root.title("File Upload GUI")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

browse_button = tk.Button(frame, text="Browse and Upload", command=browse_file)
browse_button.grid(row=0, column=0, padx=5)

file_label = tk.Label(frame, text="No file selected", wraplength=300)
file_label.grid(row=0, column=1, padx=5)

root.mainloop()
