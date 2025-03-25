import os
import re
import sys
import json
import time
import random
import asyncio
import requests
import subprocess
import urllib.parse
import yt_dlp
import cloudscraper
from logs import logging
from bs4 import BeautifulSoup
import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

cookies_file_path= "youtube_cookies.txt"

async def show_random_emojis(message):
    emojis = ['🐼', '🐶', '🐅', '⚡️', '🚀', '✨', '💥', '☠️', '🥂', '🍾']
    emoji_message = await message.reply_text(' '.join(random.choices(emojis, k=1)))
    return emoji_message
    
credit ="𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎" 
# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Inline keyboard for start command
keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="📞 Contact", url="https://t.me/Nikhil_saini_khe"),
            InlineKeyboardButton(text="🛠️ Help", url="https://t.me/+3k-1zcJxINYwNGZl"),
        ],
    ]
)

# Image URLs for the random image feature
image_urls = [
    "https://tinypic.host/images/2025/03/18/YouTube-Logo.wine.png",
    "https://tinypic.host/images/2025/02/07/DeWatermark.ai_1738952933236-1.png",
    # Add more image URLs as needed
]


@bot.on_message(filters.command(["help"]))
async def txt_handler(client: Client, m: Message):
    await bot.send_message(m.chat.id, text= (
        "<pre><code>Congrats! You are using 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎:</code></pre>\n┣\n"
        "┣⪼01. Send /start - To Check Bot \n┣\n"
        "┣⪼02. Send /logs - To see Bot Working Logs\n┣\n"
        "┣⪼03. Send /cookies - To update YT cookies.\n┣\n"
        "┣⪼04. Send /stop - Stop the Running Task. 🚫\n┣\n"
        "┣⪼🔗  Direct Send Link For Extract (with https://)\n┣\n"
        "<pre><code>If you have any questions, feel free to ask! 💬</code></pre>"
        )
    ) 

@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):
    await m.reply_text(
        "Please upload the cookies file (.txt format).",
        quote=True
    )

    try:
        # Wait for the user to send the cookies file
        input_message: Message = await client.listen(m.chat.id)

        # Validate the uploaded file
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("Invalid file type. Please upload a .txt file.")
            return

        # Download the cookies file
        downloaded_path = await input_message.download()

        # Read the content of the uploaded file
        with open(downloaded_path, "r") as uploaded_file:
            cookies_content = uploaded_file.read()

        # Replace the content of the target cookies file
        with open(cookies_file_path, "w") as target_file:
            target_file.write(cookies_content)

        await input_message.reply_text(
            "✅ Cookies updated successfully.\n📂 Saved in `youtube_cookies.txt`."
        )

    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")
        
# Start command handler
@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, message: Message):
    random_image_url = random.choice(image_urls)
    caption = (
        f"🌟 Welcome {0}! 🌟\n\n➽ I am Powerful YouTube Uploader Bot 📥\n\n➽ 𝐔𝐬𝐞 /help for use this Bot.\n\n𝐌𝐚𝐝𝐞 𝐁𝐲 : 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎 🦁"
    )
    
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=random_image_url,
        caption=caption,
        reply_markup=keyboard
    )

@bot.on_message(filters.command(["logs"]) )
async def send_logs(bot: Client, m: Message):
    try:
        with open("logs.txt", "rb") as file:
            sent= await m.reply_text("**📤 Sending you ....**")
            await m.reply_document(document=file)
            await sent.delete(True)
    except Exception as e:
        await m.reply_text(f"Error sending logs: {e}")

@bot.on_message(filters.command(["stop"]) )
async def restart_handler(_, m):
    await m.reply_text("⌈✨『𝚂𝚃𝙾𝙿𝙿𝙴𝙳』✨⌋", True)
    os.execl(sys.executable, sys.executable, *sys.argv)
         
@bot.on_message(filters.text & filters.private)
async def text_handler(bot: Client, m: Message):
    if m.from_user.is_bot:
        return
    links = m.text
    match = re.search(r'https?://\S+', links)
    if match:
        link = match.group(0)
    else:
        await m.reply_text("<pre><code>Invalid link format.</code></pre>")
        return
        
    editable = await m.reply_text(f"<pre><code>**🔹Processing your link...\n🔁Please wait...⏳**</code></pre>")
    await m.delete()

    await editable.edit("<pre><code>╭━━━━❰ᴇɴᴛᴇʀ ʀᴇꜱᴏʟᴜᴛɪᴏɴ❱━━➣ </code></pre>\n┣━━⪼ send `144`  for 144p\n┣━━⪼ send `240`  for 240p\n┣━━⪼ send `360`  for 360p\n┣━━⪼ send `480`  for 480p\n┣━━⪼ send `720`  for 720p\n┣━━⪼ send `1080` for 1080p\n┣━━⪼ send `mp3` for MP3 format\n<pre><code>╰━━⌈⚡[`🦋🇸‌🇦‌🇮‌🇳‌🇮‌🦋`]⚡⌋━━➣ </code></pre>")
    input2: Message = await bot.listen(editable.chat.id, filters=filters.text & filters.user(m.from_user.id))
    raw_text2 = input2.text
    quality = f"{raw_text2}p"
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080"
        elif raw_text2.lower() == "mp3":
            res = "MP3"
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    if raw_text2.lower() == "mp3":
        ytf = "b[ext=mp3]/b[ext=m4a]/b[ext=webm]/b[ext=opus]"
    else:
        ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"

    await editable.edit("🌅Send ☞ `Thumb URL` for **Thumbnail**\n\n🎞️Send ☞ `no` for **video** format\n\n📁Send ☞ `No` for **Document** format")
    input6 = message = await bot.listen(editable.chat.id, filters=filters.text & filters.user(m.from_user.id))
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    count = 1
    arg = 1
    try:
        Vxy = link.replace("www.youtube-nocookie.com/embed", "youtu.be")
        url = Vxy

        oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
        response = requests.get(oembed_url)
        print("Response content:", response.content)

        audio_title = response.json().get('title', 'YouTube Video')
        name = f'{audio_title[:60]}'

        if "youtube.com" in url or "youtu.be" in url:
            if raw_text2.lower() == "mp3":
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" "{url}" -o "{name}.mp3"'
                cc = f'🎵𝐓𝐢𝐭𝐥𝐞 » `{name}` .mp3\n🔗𝐋𝐢𝐧𝐤 » <a href="{link}">__**Click Here to Listen**__</a>\n\n🌟𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎'
                print(f"Running command: {cmd}")
                os.system(cmd)
                if os.path.exists(f'{name}.mp3'):
                    print(f"File {name}.mp3 exists, attempting to send...")
                    try:
                        await editable.delete()
                        await bot.send_document(chat_id=m.chat.id, document=f'{name}.mp3', caption=cc)
                        os.remove(f'{name}.mp3')
                    except Exception as e:
                        print(f"Error sending document: {str(e)}")
                else:
                    print(f"File {name}.mp3 does not exist.")
                    
            else:
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" "{url}" -o "{name}.mp4"'
                cc = f'🎞️𝐓𝐢𝐭𝐥𝐞 » `{name}` .mp4\n🔗𝐋𝐢𝐧𝐤 » <a href="{link}">__**Click Here to Watch Stream**__</a>\n\n🌟𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎'
                emoji_message = await show_random_emojis(message)
                Show = f"**⚡Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ...⏳**\n\n🔗𝐋𝐢𝐧𝐤 » {link}\n\n✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎"
                prog = await m.reply_text(Show, disable_web_page_preview=True)
                res_file = await helper.download_video(url, cmd, name)
                filename = res_file
                await prog.delete(True)
                await emoji_message.delete()
                await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                count += 1
                time.sleep(1)

    except Exception as e:
        Error = f"⚠️𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐈𝐧𝐭𝐞𝐫𝐮𝐩𝐭𝐞𝐝\n\n📚𝐓𝐢𝐭𝐥𝐞 » `{name}`\n\n🔗𝐋𝐢𝐧𝐤 » ⚡<a href='{link}'>__**Click Here to Watch Stream**__</a>\n\n✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎"
        await m.reply_text(Error, disable_web_page_preview=True)
        pass

bot.run()
if __name__ == "__main__":
    asyncio.run(main())
