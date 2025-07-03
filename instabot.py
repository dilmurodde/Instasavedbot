import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8053069809:AAFpMKtnbIT0-2zKiQ38rKFurpDW1T4rnDE"

logging.basicConfig(level=logging.INFO)

def download_instagram_video(insta_url):
    response = requests.get(f"https://igram.io/i/{insta_url}", headers={"User-Agent": "Mozilla/5.0"})
    if "video/mp4" in response.text:
        start = response.text.find("https://")
        end = response.text.find(".mp4") + 4
        return response.text[start:end]
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Assalomu alaykum!
Instagram videosining havolasini yuboring, yuklab beraman.")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "instagram.com" not in url:
        await update.message.reply_text("❗ Iltimos, Instagram havolasini yuboring.")
        return
    await update.message.reply_text("⏳ Video yuklanmoqda...")
    video = download_instagram_video(url)
    if video:
        await update.message.reply_video(video=video)
    else:
        await update.message.reply_text("⚠️ Video topilmadi yoki havola noto‘g‘ri.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.run_polling()
