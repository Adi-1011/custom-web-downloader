import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

import subprocess
import sys

# Auto-install required packages
def ensure_package(pkg_name):
    try:
        __import__(pkg_name)
    except ImportError:
        print(f"📦 Installing missing package: {pkg_name}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg_name])

# List all required packages
required_packages = ["yt_dlp"]

for pkg in required_packages:
    ensure_package(pkg)


from downloader import custom_download

SETTINGS_FILE = "settings.json"

# Load or create settings
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    else:
        return {"save_path": os.getcwd()}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

settings = load_settings()

# GUI starts here
root = tk.Tk()
root.title("Custom Web Downloader")
root.geometry("600x300")

# URL Input
tk.Label(root, text="Enter Video URL:", font=("Arial", 12)).pack(pady=10)
url_entry = tk.Entry(root, width=60, font=("Arial", 12))
url_entry.pack()

# Display current download path
path_label = tk.Label(root, text=f"Save to: {settings['save_path']}", font=("Arial", 10))
path_label.pack(pady=5)

# Change location
def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        settings["save_path"] = folder
        save_settings(settings)
        path_label.config(text=f"Save to: {folder}")

tk.Button(root, text="Change Download Folder", command=choose_folder).pack(pady=5)

# Download button
def start_download():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Missing URL", "Please enter a video URL.")
        return

    try:
        custom_download(url, settings["save_path"], filename="downloaded_video")
        messagebox.showinfo("Success", "Download complete!")
    except FileNotFoundError as e:
        messagebox.showerror("FFmpeg Missing", f"{e}\n\nPlease ensure FFmpeg is present in the assets folder or installed on your system.")
    except Exception as e:
        messagebox.showerror("Download Failed", str(e))


tk.Button(root, text="Download", font=("Arial", 12), command=start_download).pack(pady=20)

root.mainloop()
