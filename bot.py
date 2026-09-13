import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 1. Flask Web Server (for Render deployment & health checks)
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is alive!", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# 2. Telegram Bot Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Your Telegram bot is active and working!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Get command information\n"
        "/echo [message] - Repeat back your message"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        user_text = " ".join(context.args)
        await update.message.reply_text(f" You said: {user_text}")
    else:
        await update.message.reply_text("Please provide a message after /echo (e.g., `/echo hello`)")

# 3. Main Execution Block
if __name__ == "__main__":
    # Start web server in background thread
    threading.Thread(target=run_flask, daemon=True).start()

    # Uses Environment Variable on Render if set; defaults to your token locally
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8801059960:AAHK3yMpeKRVbP5zb06t7GIJCncEkENeDG0")

    # Build bot application
    bot_app = ApplicationBuilder().token(TOKEN).build()

    # Register handlers
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("help", help_command))
    bot_app.add_handler(CommandHandler("echo", echo))

    print("Bot is starting...")
    bot_app.run_polling(drop_pending_updates=True)