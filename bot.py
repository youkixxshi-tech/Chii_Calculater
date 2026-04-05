import re
import os
from flask import Flask
from threading import Thread
from simpleeval import simple_eval
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Render Web Service အတွက် Flask Port Fix
app_web = Flask('')

@app_web.route('/')
def home():
    return "Cute Calc Bot is Live! 💕"

def run_web():
    # Render မှာ Port Error မတက်အောင် 0.0.0.0 နဲ့ 10000 ကို သုံးပေးရပါတယ်
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

# --- မင်းရဲ့ Bot Token ကို သေချာထည့်ပါ ---
TOKEN = "8791977854:AAFJk2nh9QZOAygeQcQqH2ojse2FtCLcd2g"

def clean_and_calculate(expression):
    # × နဲ့ ÷ ကို Python နားလည်အောင် ပြောင်းတာပါ
    cleaned = expression.replace('×', '*').replace('÷', '/')
    try:
        # simple_eval က တွက်ချက်ပေးမှာပါ
        return simple_eval(cleaned)
    except:
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update or not update.message or not update.message.text:
        return

    user_text = update.message.text
    
    # သင်္ချာပုံစံတွေကို ရှာဖွေမယ်
    math_patterns = re.findall(r'[0-9+\-*/×÷.\s]{3,}', user_text)
    calc_results = []
    
    for item in math_patterns:
        item = item.strip()
        # အပေါင်း၊ အနှုတ်၊ အမြှောက်၊ အစား တစ်ခုခုပါမှ တွက်မယ်
        if any(op in item for op in "+-*/×÷"):
            res = clean_and_calculate(item)
            if res is not None:
                if isinstance(res, float): res = round(res, 2)
                calc_results.append(f"✨ {item} = **{res}**")

    if calc_results:
        response_text = "🎀 **Calculator Result** 🎀\n\n"
        response_text += "\n".join(calc_results)
        response_text += "\n\n💕 Have a sweet day, Sis! ✨"

        keyboard = [[InlineKeyboardButton("🗑 Delete", callback_data="delete_msg")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            response_text, 
            parse_mode='Markdown', 
            reply_markup=reply_markup
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "delete_msg":
        await query.message.delete()

if __name__ == "__main__":
    # Flask ကို Background မှာအရင် Run မယ်
    Thread(target=run_web).start()
    
    # Bot ကို စတင်မယ်
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot is starting...")
    app.run_polling()
