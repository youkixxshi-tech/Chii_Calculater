import os
import re
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- UptimeRobot အတွက် Flask ---
app_web = Flask('')

@app_web.route('/')
def home():
    return "Chii Calculator is Online! ✨"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

# --- မင်းရဲ့ Bot Token ကို ဒီမှာထည့် ---
TOKEN = "8791977854:AAFJk2nh9QZOAygeQcQqH2ojse2FtCLcd2g"

async def handle_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    # User ရိုက်လိုက်တဲ့ စာသား (ဥပမာ 39693x3)
    user_input = update.message.text
    
    # သင်္ချာတွက်လို့ရအောင် x ကို * ပြောင်း၊ ÷ ကို / ပြောင်းမယ်
    calc_text = user_input.replace('×', '*').replace('x', '*').replace('÷', '/')

    try:
        # ဂဏန်းနဲ့ သင်္ချာသင်္ကေတတွေပဲ ပါမပါ Regex နဲ့ စစ်မယ်
        if re.match(r'^[0-9+\-*/().\s]+$', calc_text):
            result = eval(calc_text)
            
            # မင်းပြတဲ့ ပုံစံအတိုင်း စာသားကို ပြင်မယ်
            response_text = (
                f"🎀 Calculator Result 🎀\n\n"
                f"✨ {user_input} = {result}\n\n"
                f"💕 Have a sweet day, Sis! ✨"
            )
            
            # Delete Button လေး ထည့်မယ်
            keyboard = [[InlineKeyboardButton("🗑️ Delete", callback_data="delete_msg")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(response_text, reply_markup=reply_markup)
    except:
        # မှားရိုက်ရင် ဘာမှပြန်မလုပ်ဘဲ နေလို့ရတယ် (သို့မဟုတ်) Error ပြလို့ရတယ်
        pass

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "delete_msg":
        await query.message.delete()

if __name__ == "__main__":
    Thread(target=run_web).start()
    
    app = Application.builder().token(TOKEN).build()
    
    # Message တွေ့တာနဲ့ တွက်ချက်ပေးမယ့် Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_calc))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Chii Calculator Bot is Live!")
    app.run_polling()
