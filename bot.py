import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler, 
    filters, 
    ContextTypes
)

# 1. Flask Web Server (Render Health Check සඳහා)
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is alive!", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# --- CONFIGURATION LINKS ---
CHANNEL_LINK = "https://t.me/solis2001"
GROUP_LINK = "https://t.me/solis2002"
WHATSAPP_LINK = "https://whatsapp.com/channel/0029Vb8SAPNDOQIU506xeF0N" # ⚠️ මෙතැනට ඔබේ WhatsApp Group Link එක දාන්න

# Interactive Menu Keyboard (Bubble/Tab Buttons UI)
def get_main_menu():
    keyboard = [
        [
            InlineKeyboardButton("📜 Rules (නීති)", callback_data="btn_rules"),
            InlineKeyboardButton("ℹ️ Help (උදව්)", callback_data="btn_help")
        ],
        [
            InlineKeyboardButton("📢 Telegram Channel", url=CHANNEL_LINK),
            InlineKeyboardButton("👥 Telegram Group", url=GROUP_LINK)
        ],
        [
            InlineKeyboardButton("📲 Join WhatsApp Status Group", url=WHATSAPP_LINK)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# 1. /start Command (ලස්සන Interactive Menu එක ලබා දීම)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "👋 **Solis Status Community Bot වෙත සාදරයෙන් පිළිගනිමු!**\n\n"
        "ඔබට අවශ්‍ය තොරතුරු ලබා ගැනීමට පහත **Buttons (Tabs)** ක්ලික් කරන්න:"
    )
    await update.message.reply_text(
        welcome_msg, 
        reply_markup=get_main_menu(), 
        parse_mode="Markdown"
    )

# 2. Buttons මත Click කළ විට ක්‍රියාත්මක වන කොටස (Callback Handler)
async def button_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "btn_rules":
        rules_text = (
            "📌 **Solis Community Rules (නීති මාලාව)**\n\n"
            "1. අනවශ්‍ය හෝ අසභ්‍ය වීඩියෝ/පෝස්ට් දැමීමෙන් සම්පූර්ණයෙන්ම වළකින්න.\n"
            "2. අවසරයකින් තොරව වෙනත් Promos හෝ Links දැමීම තහනම්.\n"
            "3. සියලුම සාමාජිකයන්ට ගෞරවයෙන් සලකන්න.\n"
            "4. Status Videos ඉල්ලීම් (Requests) සඳහා පමණක් මෙම සමූහය භාවිතා කරන්න."
        )
        await query.message.reply_text(rules_text, reply_markup=get_main_menu(), parse_mode="Markdown")

    elif query.data == "btn_help":
        help_text = (
            "ℹ️ **Solis Bot Help Center**\n\n"
            "• පහත Buttons භාවිතයෙන් කෙළින්ම Channels & Groups වලට එකතු විය හැක.\n"
            "• Group එක තුළදී `/rules` හෝ `/help` ලෙස Type කරද තොරතුරු ලබාගත හැක."
        )
        await query.message.reply_text(help_text, reply_markup=get_main_menu(), parse_mode="Markdown")

# 3. /rules Command (Type කරද්දී)
async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rules_text = (
        "📌 **Solis Community Rules (නීති මාලාව)**\n\n"
        "1. අනවශ්‍ය හෝ අසභ්‍ය වීඩියෝ/පෝස්ට් දැමීමෙන් සම්පූර්ණයෙන්ම වළකින්න.\n"
        "2. අවසරයකින් තොරව වෙනත් Promos හෝ Links දැමීම තහනම්.\n"
        "3. සියලුම සාමාජිකයන්ට ගෞරවයෙන් සලකන්න.\n"
        "4. Status Videos ඉල්ලීම් (Requests) සඳහා පමණක් මෙම සමූහය භාවිතා කරන්න."
    )
    await update.message.reply_text(rules_text, parse_mode="Markdown")

# 4. /help Command (Type කරද්දී)
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "ℹ️ **Solis Bot Help Center**\n\n"
        "ඔබට අවශ්‍ය ලිංක් ලබා ගැනීමට පහත Buttons ක්ලික් කරන්න:"
    )
    await update.message.reply_text(help_text, reply_markup=get_main_menu(), parse_mode="Markdown")

# 5. Auto Welcome New Members (Group එකට කෙනෙක් එද්දී Auto Message එකක් යාම)
async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            continue
            
        welcome_text = (
            f"👋 ආයුබෝවන් {member.first_name}! **Solis Community Group** (`@solis2002`) එකට සාදරයෙන් පිළිගනිමු.\n\n"
            "අපගේ දෛනික Status Videos ලබා ගැනීමට පහත සබැඳි භාවිතා කරන්න."
        )
        await update.message.reply_text(welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")

# MAIN EXECUTION BLOCK
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()

    # Render Environment Variable එකෙන් පමණක් Token එක ලබා ගැනීම
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise ValueError("❌ ආරක්ෂක දෝෂයක්: TELEGRAM_BOT_TOKEN Environment Variable එක සකසා නැත!")

    bot_app = ApplicationBuilder().token(TOKEN).build()

    # Handlers Register කිරීම
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("rules", rules_command))
    bot_app.add_handler(CommandHandler("help", help_command))
    bot_app.add_handler(CallbackQueryHandler(button_click_handler))
    bot_app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))

    print("Bot is running smoothly...")
    bot_app.run_polling(drop_pending_updates=True)
