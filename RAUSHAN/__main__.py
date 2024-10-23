import asyncio
import importlib
from pyrogram import Client, idle
from RAUSHAN.helper import join
from RAUSHAN.modules import ALL_MODULES
from RAUSHAN import clients, app, ids
from flask import Flask
import threading

# Flask app initialize kar rahe hain
flask_app = Flask(__name__)

# Flask app ka ek basic route
@flask_app.route('/')
def home():
    return "Flask app running on port 8000"

# Flask app ko alag thread mein run karne ka function
def run_flask():
    flask_app.run(host="0.0.0.0", port=8000)

# Bot ke start karne ka async function
async def start_bot():
    await app.start()
    print("LOG: Founded Bot token Booting Zeus.")
    # Sabhi modules ko import kar rahe hain
    for all_module in ALL_MODULES:
        importlib.import_module("RAUSHAN.modules." + all_module)
        print(f"Successfully Imported {all_module} 💥")
    
    # Sabhi clients ko start kar rahe hain
    for cli in clients:
        try:
            await cli.start()
            ex = await cli.get_me()
            await join(cli)
            print(f"Started {ex.first_name} 🔥")
            ids.append(ex.id)
        except Exception as e:
            print(f"Error: {e}")
    
    # Bot ko idle mode mein daal rahe hain taaki continuous run ho
    await idle()

# Flask app ko alag thread mein start kar rahe hain
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# Bot ko asyncio loop ke through run kar rahe hain
loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())
