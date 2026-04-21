import os
OPENROUTER_API_KEY = "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"
TELEGRAM_TOKEN = "8771381084:AAEDz9ycvsogdyxPMKRkpTA9__1F9ESeBu0"

API_URL = "https://openrouter.ai/api/v1/chat/completions"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Trading Bot Active!\n\n"
        "Ask me anything about:\n"
        "- Crypto (BTC, ETH, Solana)\n"
        "- Forex (EUR/USD, GBP/USD)\n"
        "- Stocks or market trends\n\n"
        "Just type your question!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.chat.send_action(action="typing")
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {"role": "system", "content": "You are a trading analyst. Give clear, practical answers."},
            {"role": "user", "content": user_message}
        ]
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        ai_response = result["choices"][0]["message"]["content"]
        await update.message.reply_text(ai_response)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot is running!")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
