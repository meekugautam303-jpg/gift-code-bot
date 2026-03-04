from telethon import TelegramClient, events
import re
from flask import Flask
import threading
from collections import deque

# --- 1. Server Setup (Taaki bot 24/7 chale) ---
app = Flask(__name__)
@app.route('/')
def home(): 
    return "Super Smart Preserver Active"

def run_server(): 
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_server).start()

# --- 2. Configuration ---
api_id = 37535560
api_hash = 'ea928ae0b20301569d4d348b5383abf5'
source_channels = ['sanzi91clubvip', 'VIP91_55Hub', 'amangidtosw']
my_channel = '@predection_king11' 

client = TelegramClient('mera_userbot', api_id, api_hash)

# Naya Smart Duplicate Filter (Pichle 100 codes yaad rakhega)
recent_codes = deque(maxlen=100)

@client.on(events.NewMessage)
async def handler(event):
    msg = event.raw_text
    sender = await event.get_chat()
    u_name = getattr(sender, 'username', '')

    # Check if message is from your target channels
    if u_name in source_channels or "!test" in msg.lower():
        
        # Regex filter jo sirf 8 se 35 characters lambe code ko pakdega
        code_pattern = r'\b[A-Z0-9]{8,35}\b'
        codes = re.findall(code_pattern, msg)

        # --- RULE 1: Instructions & Hype Messages ---
        # Agar message me koi gift code nahi hai, lekin "Note", "Code", "Coming" likha hai
        hype_keywords = ["AGAIN", "DROPPING", "CLAIM", "READY", "COMING", "NOTE", "EACH", "TOP", "FIRST", "GIFTCODE", "CODE"]
        
        if any(word in msg.upper() for word in hype_keywords) and not codes:
            # Kisi bhi tarah ka link delete karo aur Same to Same send karo
            clean_hype = re.sub(r'https?://\S+', '', msg)
            await client.send_message(my_channel, clean_hype.strip())
            return

        # --- RULE 2: Gift Codes (Exact Same Layout & Smart Duplicate Check) ---
        if codes or "!test" in msg.lower():
            
            # --- PERFECT DUPLICATE LOCK ---
            # Check karega ki kya inme se koi bhi code pehle aa chuka hai
            is_duplicate = False
            for c in codes:
                if c in recent_codes:
                    is_duplicate = True
                    break
            
            # Agar duplicate hai (Sanzi wale code VIP ne dale), toh Ignore karega
            if is_duplicate and "!test" not in msg.lower():
                return
            
            # Agar naye codes hain (Jaise VIP ne 55 Club ya IN999 ke dale), toh Memory me save kar lega
            for c in codes:
                recent_codes.append(c)

            # Step A: Remove Links (Koi bhi URL hoga toh delete ho jayega)
            clean_msg = re.sub(r'https?://\S+', '', msg)
            
            # Step B: Wrap Codes in Mono
            def wrap_code(match):
                return f"`{match.group(0)}`"
            
            final_msg = re.sub(code_pattern, wrap_code, clean_msg)

            # Step C: Original message EXACTLY waisa hi forward kar do
            await client.send_message(my_channel, final_msg.strip())

client.start()
client.run_until_disconnected()
