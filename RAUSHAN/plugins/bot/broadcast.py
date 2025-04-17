from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pymongo import MongoClient
import asyncio
from pyrogram.errors import FloodWait
from RAUSHAN import app

OWNER_ID = 8143754205


MONGO_URI = "mongodb+srv://Clonebot:purviclone@cluster0.d33sftp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


client = MongoClient(MONGO_URI)
db = client["broadcastDB"]
users_col = db["users"]
groups_col = db["groups"]

# --- SAVE USER ON /start ---
@app.on_message(filters.command("start") & filters.private)
async def save_user(client: Client, message: Message):
    users_col.update_one(
        {"_id": message.chat.id},
        {"$set": {"name": message.from_user.first_name}},
        upsert=True
    )
    # No reply


# --- GROUP ADDED ---
@app.on_message(filters.new_chat_members)
async def on_new_chat_members(client: Client, message: Message):
    bot_id = (await client.get_me()).id
    if bot_id in [user.id for user in message.new_chat_members]:
        chat_id = message.chat.id
        chat_title = message.chat.title
        groups_col.update_one(
            {"_id": chat_id},
            {"$set": {"title": chat_title}},
            upsert=True
        )


# --- GROUP REMOVED ---
@app.on_message(filters.left_chat_member)
async def on_left_chat_member(client: Client, message: Message):
    bot_id = (await client.get_me()).id
    if message.left_chat_member.id == bot_id:
        chat_id = message.chat.id
        groups_col.delete_one({"_id": chat_id})


# --- BROADCAST ---
@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_message(client: Client, message: Message):
    reply = message.reply_to_message
    text = message.text.split(None, 1)[1] if len(message.command) > 1 else None

    if not reply and not text:
        return await message.reply_text("**ɢɪᴠᴇ ᴀ ᴍᴇssᴀɢᴇ / ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ**")

    progress = await message.reply_text("**ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ....**")

    sent_groups, sent_users, failed = 0, 0, 0

    user_ids = [doc["_id"] for doc in users_col.find()]
    group_ids = [doc["_id"] for doc in groups_col.find()]
    all_ids = user_ids + group_ids

    for chat_id in all_ids:
        try:
            if reply:
                await reply.copy(chat_id)
            else:
                await client.send_message(chat_id, text=text)
            
            if chat_id < 0:
                sent_groups += 1
            else:
                sent_users += 1

            await asyncio.sleep(0.2)
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
        except:
            failed += 1

    await progress.edit_text(
        f"**⊚ ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ :**\n\n"
        f"**➻ ɢʀᴏᴜᴘs :** {sent_groups}\n"
        f"**➻ ᴜsᴇʀs :** {sent_users}\n"
        f"**➻ ғᴀɪʟᴇᴅ :** {failed}",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]]
        )
    )

# Non-owner handling
@app.on_message(filters.command("broadcast") & ~filters.user(OWNER_ID))
async def not_allowed(_, message: Message):
    await message.reply_text("**ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.**")


# --- STATS ---
@app.on_message(filters.command("stats"))
async def show_stats(client: Client, message: Message):
    total_users = users_col.count_documents({})
    total_groups = groups_col.count_documents({})

    await message.reply_text(
        f"**⊚ ᴄᴜʀʀᴇɴᴛ ʙᴏᴛ sᴛᴀᴛs :**\n\n"
        f"**➻ ᴜsᴇʀs :** {total_users}\n"
        f"**➻ ɢʀᴏᴜᴘs :** {total_groups}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/purvi_support"),
                    InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close"),
                ]
            ]
        )
    )


# Callback handler for "Close" button
@app.on_callback_query(filters.regex("close"))
async def close_callback(_, query: CallbackQuery):
    try:
        await query.message.delete()
    except:
        pass
    try:
        await query.answer()
    except:
        pass
