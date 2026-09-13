import os
import threading
from flask import Flask
from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    BotCommand, 
    BotCommandScopeAllPrivateChats, 
    BotCommandScopeAllGroupChats
)
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes
)

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is alive!", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# --- CONFIGURATION LINKS ---
CHANNEL_USERNAME = "@solis2001"
CHANNEL_LINK = "https://t.me/solis2001"
GROUP_LINK = "https://t.me/solis2002"
WHATSAPP_LINK = "https://whatsapp.com/channel/0029Vb8SAPNDOQIU506xeF0N" # ⚠️ ඔබේ WhatsApp Group Link එක මෙතැනට දාන්න

# Command Scopes සකස් කිරීම (Group එකේ සහ Private chat එකේ පෙනෙන Commands වෙන් කිරීම)
async def post_init(application):
    # Private chat වල පෙනෙන Commands (Admin සඳහා /postchannel සමඟ)
    private_commands = [
        BotCommand("start", "Start the bot & get links"),
        BotCommand("whatsapp", "Get WhatsApp group link"),
        BotCommand("rules", "View community rules"),
        BotCommand("help", "Show help menu"),
        BotCommand("postchannel", "Post status to channel (Admin Only)")
    ]
    await application.bot.set_my_commands(private_commands, scope=BotCommandScopeAllPrivateChats())
    
    # Group චැට් වල පෙනෙන Commands (/postchannel මෙහි නොමැත, එიტොයින් Group එකේ එය පෙන්වන්නේ නැත)
    group_commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("whatsapp", "Get WhatsApp group link"),
        BotCommand("rules", "View community rules"),
        BotCommand("help", "Show help menu")
    ]
    await application.bot.set_my_commands(group_commands, scope=BotCommandScopeAllGroupChats())

# 1. /start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Telegram Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("👥 Join Telegram Group", url=GROUP_LINK)],
        [InlineKeyboardButton("📲 Join WhatsApp Status Group", url=WHATSAPP_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 **Solis Status Hub වෙත සාදරයෙන් පිළිගනිමු!**\n\n"
        "අපගේ නාලිකාව හරහා දිනපතා අලුත්ම WhatsApp Status Videos ලබාගත හැක. පහත බොත්තම් මගින් අපගේ සමූහයන්ට එකතු වන්න.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# 2. /rules Command
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rules_text = (
        "📌 **Solis Community Rules (නීති මාලාව)**\n\n"
        "1. අනවශ්‍ය හෝ අසභ්‍ය වීඩියෝ/පෝස්ට් දැමීමෙන් සම්පූර්ණයෙන්ම වළකින්න.\n"
        "2. අවසරයකින් තොරව වෙනත් Promos හෝ Links දැමීම තහනම්.\n"
        "3. සියලුම සාමාජිකයන්ට ගෞරවයෙන් සලකන්න.\n"
        "4. Status Videos ඉල්ලීම් (Requests) සඳහා පමණක් මෙම සමූහය භාවිතා කරන්න."
    )
    await update.message.reply_text(rules_text, parse_mode="Markdown")

# 3. /whatsapp Command
async def whatsapp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📲 Join WhatsApp Status Group Now", url=WHATSAPP_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👇 පහත බොත්තම ක්ලික් කර අපගේ නිල WhatsApp Status Group එකට එකතු වන්න:",
        reply_markup=reply_markup
    )

# 4. /help Command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "ℹ️ **Bot Commands ලැයිස්තුව:**\n\n"
        "/start - Bot ආරම්භ කර ප්‍රධාන සබැඳි ලබා ගැනීමට\n"
        "/rules - Group එකේ නීති බැලීමට\n"
        "/whatsapp - WhatsApp Group එකට එකතු වීමට\n"
        "/help - මෙම උදව් පණිවිඩය බැලීමට"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# 5. Auto Welcome New Members (Group එකට කෙනෙක් එද්දී ස්වයංක්‍රීයව Buttons සමඟ පණිවිඩය යාම)
async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            continue
            
        keyboard = [
            [InlineKeyboardButton("📢 Telegram Channel", url=CHANNEL_LINK)],
            [InlineKeyboardButton("📲 WhatsApp Group", url=WHATSAPP_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = (
            f"👋 ආයුබෝවන් {member.first_name}! **Solis Community Group** (`@solis2002`) එකට සාදරයෙන් පිළිගනිමු.\n\n"
            "අපගේ දෛනික Status Videos සහ තවත් දේ ලබා ගැනීමට ඉහත සබැඳි භාවිතා කරන්න."
        )
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# 6. /postchannel Command (රහසිගතයි: Bot සමඟ ඇති Private Chat එකේදී පමණක් ක්‍රියාත්මක වේ)
async def post_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ආරක්ෂක පරීක්ෂාව: Group එක içinde මෙය වැළැක්වීම
    if update.effective_chat.type != "private":
        await update.message.reply_text("⚠️ මෙම Command එක Group එක ඇතුළේ භාවිතා කළ නොහැක. කරුණාකර Bot සමඟ ඇති Private Chat එකට පැමිණ එය භාවිතා කරන්න.")
        return

    keyboard = [
        [InlineKeyboardButton("📲 Join WhatsApp Group", url=WHATSAPP_LINK)],
        [InlineKeyboardButton("💬 Chat in Telegram Group", url=GROUP_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    post_message = (
        "🎬 **New WhatsApp Status Video Uploaded!**\n\n"
        "🔥 අලුත්ම ට්‍රෙන්ඩින් Status Videos නරඹන්න සහ ඩවුන්ලෝඩ් කරගන්න අපගේ WhatsApp සහ Telegram සමූහයන් සමඟ රැඳී සිටින්න."
    )

    try:
        await context.bot.send_message(
            chat_id=CHANNEL_USERNAME,
            text=post_message,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        await update.message.reply_text("✅ Channel (`@solis2001`) එකට Post එක සාර්ථකව යැවුවා!")
    except Exception as e:
        await update.message.reply_text(
            f"❌ Post එක යැවීම අසාර්ථකයි.\nError: {e}\n\n"
            "⚠️ කරුණාකර Bot ව `@solis2001` Channel එකේ Administrator කෙනෙක් ලෙස එකතු කර ඇත්දැයි පරීක්ෂා කරන්න."
        )

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()

    # 100% Security: Render Environment Variable එකෙන් පමණක් Token එක ලබා ගැනීම (Hardcoding නැත)
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise ValueError("❌ ආරක්ෂක දෝෂයක්: TELEGRAM_BOT_TOKEN Environment Variable එක සකසා නැත!")

    bot_app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    # Handlers Register කිරීම
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("rules", rules))
    bot_app.add_handler(CommandHandler("whatsapp", whatsapp))
    bot_app.add_handler(CommandHandler("help", help_command))
    bot_app.add_handler(CommandHandler("postchannel", post_channel))
    bot_app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))

    print("Bot is running securely...")
    bot_app.run_polling(drop_pending_updates=True)
