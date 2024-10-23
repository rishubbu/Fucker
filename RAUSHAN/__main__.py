import asyncio
from pyrogram import Client, idle
from RAUSHAN.helper import join
from RAUSHAN import clients, app, ids
from flask import Flask
import threading
import requests
import time

# Flask app initialize kar rahe hain
flask_app = Flask(__name__)

# Flask app ka ek basic route
@flask_app.route('/')
def home():
    return "Flask app running on port 8000"

# Flask app ko alag thread mein run karne ka function
def run_flask():
    flask_app.run(host="0.0.0.0", port=8000)

# Keep-alive function jo regular ping bhejta rahega
def keep_alive():
    while True:
        try:
            requests.get("https://satya-userbot.onrender.com")
        except Exception as e:
            print(f"Ping error: {e}")
        time.sleep(300)

# Bot ke start karne ka async function
async def start_bot():
    await app.start()
    print("LOG: Founded Bot token Booting Zeus.")
    
    for cli in clients:
        try:
            await cli.start()
            ex = await cli.get_me()
            await join(cli)
            print(f"Started {ex.first_name} 🔥")
            ids.append(ex.id)
        except Exception as e:
            print(f"Error: {e}")
    
    await idle()

# Flask app ko daemon thread mein start kar rahe hain
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Keep-alive function ko daemon thread mein start kar rahe hain
keep_alive_thread = threading.Thread(target=keep_alive)
keep_alive_thread.daemon = True
keep_alive_thread.start()

# Bot ko asyncio loop ke through run kar rahe hain
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(start_bot())
