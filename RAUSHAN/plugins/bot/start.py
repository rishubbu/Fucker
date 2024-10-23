from RAUSHAN import app, API_ID, API_HASH
from config import ALIVE_PIC
from pyrogram import filters
import os
import re
import asyncio
import time
from pyrogram import *
from pyrogram.types import * 

PHONE_NUMBER_TEXT = (
    "╭────── ˹ 𝖧ᴇʟʟᴏ 𝖡ᴀʙʏ ˼ ──── ⚘\n┆⚘ 𝖧ᴇʏ, ɪ ᴀᴍ : [˹  ˼](https://t.me/KING_XUSER_BOT)\n┆⚘ 𝖬ᴏʀᴇ ᴀɴɪᴍᴀᴛɪᴏɴ,ғᴜɴ\n┊⚘ 𝖯ᴏᴡᴇʀғᴜʟ & ᴜsᴇғᴜʟʟ ᴜsᴇʀʙᴏᴛ\n╰───────────────────────\n────────────────────────\n❍ 𝖧ᴏᴡ тᴏ ᴜsᴇ тнɪs вσᴛ - [ᴄʟɪᴄᴋ ʜᴇʀᴇ](https://t.me/PURVI_SUPPORT/223) \n────────────────────────\n❍ 𝖲ᴇssɪᴏɴ 𝖦ᴇɴ вᴏᴛ ⁚ [sᴇssɪᴏɴ-ʙᴏᴛ](https://t.me/KING_STRING_SESSION_BOT) \n────────────────────────\n❍ 𝖢ʟᴏɴᴇ вσт ⁚ /clone [ sᴛʀɪɴɢ sᴇssɪᴏɴ ]\n────────────────────────\n❍ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ⏤‌‌‌‌  [˹ ᴘᴜʀᴠɪ-ᴍᴜ𝛅𝛊ᴄ™ ˼](https://t.me/purvi_support) \n────────────────────────"
)

@app.on_message(filters.command("start"))
async def hello(client: app, message):
    buttons = [
           [
                InlineKeyboardButton("˹ 𝐎ᴡɴᴇʀ ˼", url="https://t.me/ll_ALPHA_BABY_lll"),
                InlineKeyboardButton("˹ 𝐔ᴘᴅᴀᴛᴇ ˼", url="https://t.me/PURVI_SUPPORT"),
            ],
            [
                InlineKeyboardButton("˹ 𝐒ᴜᴘᴘᴏʀᴛ ˼", url="https://t.me/+Oh7OmMhAPKY5YTc9"),
                InlineKeyboardButton("˹ 𝐌ᴜsɪᴄ ˼", url="https://t.me/PURVI_MUSIV_BOT"),
            ],
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_photo(message.chat.id, ALIVE_PIC, caption=PHONE_NUMBER_TEXT, reply_markup=reply_markup)

@app.on_message(filters.command("clone"))
async def clone(bot: app, msg: Message):
    chat = msg.chat
    text = await msg.reply("ᴜsᴀɢᴇ:\n\n /clone session")
    cmd = msg.command
    phone = msg.command[1]
    try:
        await text.edit("ʀᴜᴋ ᴛʜᴏᴅᴀ sᴀ ᴀʟᴘʜᴀ ᴛᴇʀɪ ɢᴀɴᴅ ᴍᴀʀ ʀʜᴀ 👅.....✲")
                   # change this Directry according to ur repo
        client = Client(name="Melody", api_id=API_ID, api_hash=API_HASH, session_string=phone, plugins=dict(root="RAUSHAN/plugins"))
        await client.start()
        user = await client.get_me()
        await msg.reply(f" ᴊᴀ ᴘᴇʟ sᴀʙᴋᴏ ᴏʀ ʜᴀᴀ ᴀʟᴘʜᴀ ᴋᴏ ᴘᴀᴘᴀ ʙᴏʟ ᴋᴇ ᴊᴀɴᴀ 🥵 {user.first_name} 💨.")
    except Exception as e:
        await msg.reply(f"**ERROR:** `{str(e)}`\nPress /start to Start again.")
