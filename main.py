import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import json
import os
import threading
import subprocess
import sys

dark_bg = "#1e1e1e"
dark_fg = "#ffffff"
entry_bg = "#2a2a2a"
highlight_color = "#3e3e3e"
button_bg = "#3a3a3a"




def resource_path(relative_path):
    """ Get absolute path to resource (icon) for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS  # When bundled
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


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

def generate_unique_filename(base_name, download_path):
    i = 1
    while True:
        candidate = f"{base_name}_{i}.mp4"
        if not os.path.exists(os.path.join(download_path, candidate)):
            return base_name + f"_{i}"
        i += 1

def start_download():
    threading.Thread(target=threaded_download, daemon=True).start()

def dark_button(master, **kwargs):
    # Only set defaults if they are NOT passed by the userS
    kwargs.setdefault("bg", "#3a3a3a")
    kwargs.setdefault("fg", "#ffffff")
    kwargs.setdefault("activebackground", "#555555")
    kwargs.setdefault("activeforeground", "#ffffff")
    kwargs.setdefault("highlightbackground", "#1e1e1e")
    kwargs.setdefault("relief", tk.FLAT)
    kwargs.setdefault("font", ("Arial", 12))

    return tk.Button(master, **kwargs)




settings = load_settings()

# GUI starts here
root = tk.Tk()
root.iconbitmap(default=resource_path("icon.ico"))

root.title("Custom Web Downloader")
root.geometry("700x350")
root.configure(bg=dark_bg)

# URL Input
tk.Label(root, text="Enter Video URL:", font=("Arial", 12),bg=dark_bg, fg=dark_fg
).pack(pady=10)
url_entry = tk.Entry(root, width=60, font=("Arial", 12), bg=entry_bg, fg=dark_fg, insertbackground=dark_fg, highlightbackground=highlight_color, highlightcolor=highlight_color)
url_entry.pack()

# Filename Input
tk.Label(root, text="Enter Filename (optional):", font=("Arial", 10),bg=dark_bg, fg=dark_fg).pack(pady=5)
filename_entry = tk.Entry(root, width=40, font=("Arial", 10), bg=entry_bg, fg=dark_fg, insertbackground=dark_fg, highlightbackground=highlight_color, highlightcolor=highlight_color)
filename_entry.pack()


# Display current download path
path_label = tk.Label(root, text=f"Save to: {settings['save_path']}", font=("Arial", 10),bg=dark_bg, fg=dark_fg)
path_label.pack(pady=5)

# Change location
def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        settings["save_path"] = folder
        save_settings(settings)
        path_label.config(text=f"Save to: {folder}")

dark_button(root, text="Change Download Folder", command=choose_folder,).pack(pady=5)

download_button = dark_button(root, text="Download", font=("Arial", 12), command=start_download)
download_button.pack(pady=20)


progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=400, mode="determinate")
progress_bar.pack(pady=10)

progress_label = tk.Label(root, text="Progress: 0%", font=("Arial", 10),bg=dark_bg, fg=dark_fg)
progress_label.pack()



# Download button
def threaded_download():
    url = url_entry.get()
    input_name = filename_entry.get().strip()
    download_button.config(state="disabled")  # ⛔ disable during process
    if not url:
        messagebox.showwarning("Missing URL", "Please enter a video URL.")
        return
    
    # Generate filename
    if input_name:
        filename = input_name
    else:
        filename = generate_unique_filename("video_output", settings["save_path"])

    def update_progress(percent):
        progress_var.set(percent)
        progress_label.config(text=f"Progress: {percent:.1f}%")
        root.update_idletasks()

    try:
        custom_download(url, settings["save_path"], filename=filename, progress_callback=update_progress)
        messagebox.showinfo("Success", f"Download complete!\nSaved as: {filename}.mp4")
        progress_var.set(0)
        progress_label.config(text="Progress: 0%")

    except FileNotFoundError as e:
        messagebox.showerror("FFmpeg Missing", f"{e}\n\nPlease ensure FFmpeg is present in the assets folder or installed on your system.")
    except Exception as e:
        messagebox.showerror("Download Failed", str(e))
    finally:
        # Re-enable the download button
        download_button.config(state="normal")

def start_download():
    threading.Thread(target=threaded_download, daemon=True).start()

download_button = dark_button(root, text="Download", font=("Arial", 12), command=start_download)
download_button.pack(pady=20)
root.mainloop()
