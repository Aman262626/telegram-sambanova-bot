#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot with SambaNova AI
Version: 1.1.0 (Stable)
"""

import os
import logging
import requests
from datetime import timedelta
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

# ==================== CONFIGURATION ====================

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SAMBANOVA_API_KEY = os.getenv("SAMBANOVA_API_KEY")
SAMBANOVA_URL = "https://api.sambanova.ai/v1/chat/completions"
DEFAULT_MODEL = "Meta-Llama-3.1-70B-Instruct"

# ==================== LOGGING ====================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== STORAGE ====================

user_conversations = {}
user_models = {}
bot_stats = {
    "start_time": time.time(),
    "total_messages": 0,
    "total_users": set(),
    "errors": 0
}

MODELS = {
    "fast": "Meta-Llama-3.1-8B-Instruct",
    "balanced": "Meta-Llama-3.1-70B-Instruct",
    "powerful": "Meta-Llama-3.1-405B-Instruct"
}

# ==================== AI RESPONSE ====================

def get_ai_response(user_id: int, message: str) -> str:
    """Get AI response from SambaNova"""
    try:
        if user_id not in user_conversations:
            user_conversations[user_id] = []
        
        if user_id not in user_models:
            user_models[user_id] = DEFAULT_MODEL
        
        user_conversations[user_id].append({
            "role": "user",
            "content": message
        })
        
        if len(user_conversations[user_id]) > 20:
            user_conversations[user_id] = user_conversations[user_id][-20:]
        
        system_prompt = {
            "role": "system",
            "content": "You are a helpful AI assistant. Support English, Hindi, and Hinglish. Be friendly and concise."
        }
        
        response = requests.post(
            SAMBANOVA_URL,
            headers={
                "Authorization": f"Bearer {SAMBANOVA_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": user_models[user_id],
                "messages": [system_prompt] + user_conversations[user_id],
                "temperature": 0.7,
                "max_tokens": 1500
            },
            timeout=30
        )
        
        if response.status_code == 200:
            ai_message = response.json()['choices'][0]['message']['content']
            user_conversations[user_id].append({
                "role": "assistant",
                "content": ai_message
            })
            return ai_message
        else:
            bot_stats["errors"] += 1
            return f"⚠️ API Error {response.status_code}. Please try again!"
    
    except requests.exceptions.Timeout:
        bot_stats["errors"] += 1
        return "⏱️ Timeout! Please try again."
    
    except Exception as e:
        bot_stats["errors"] += 1
        logger.error(f"AI Error: {e}")
        return f"❌ Error: {str(e)}"

# ==================== COMMAND HANDLERS ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start"""
    try:
        user_name = update.effective_user.first_name or "User"
        
        keyboard = [
            [
                InlineKeyboardButton("💬 Chat", callback_data='chat'),
                InlineKeyboardButton("ℹ️ Help", callback_data='help')
            ],
            [
                InlineKeyboardButton("🤖 Model", callback_data='models'),
                InlineKeyboardButton("📊 Stats", callback_data='stats')
            ]
        ]
        
        text = f"""👋 **Hi {user_name}!**

🤖 AI Bot powered by SambaNova

**Features:**
• Multi-language (EN/HI/Hinglish)
• Conversation memory
• Multiple AI models
• Fast responses

**Commands:**
/help - Show help
/reset - Clear history
/model - Change model
/stats - Statistics

Just send any message to chat!"""
        
        await update.message.reply_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        logger.error(f"Start error: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help"""
    try:
        text = """🆘 **Help Menu**

**Commands:**
/start - Welcome message
/help - This menu
/reset - Clear conversation
/model - Change AI model
/stats - View statistics

**Usage:**
Just send any message!

**Examples:**
• "What is AI?"
• "Python code example"
• "Mujhe coding sikhao"

**Languages:**
🇬🇧 English | 🇮🇳 Hindi | 🔄 Hinglish"""
        
        if update.message:
            await update.message.reply_text(text, parse_mode='Markdown')
        elif update.callback_query:
            await update.callback_query.message.reply_text(text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Help error: {e}")

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /reset"""
    try:
        user_id = update.effective_user.id
        
        if user_id in user_conversations:
            count = len(user_conversations[user_id])
            del user_conversations[user_id]
            text = f"✅ Cleared {count} messages!"
        else:
            text = "💭 No history to clear."
        
        if update.message:
            await update.message.reply_text(text)
        elif update.callback_query:
            await update.callback_query.message.reply_text(text)
    except Exception as e:
        logger.error(f"Reset error: {e}")

async def model_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /model"""
    try:
        user_id = update.effective_user.id
        current = user_models.get(user_id, DEFAULT_MODEL)
        
        keyboard = [
            [InlineKeyboardButton("⚡ Fast (8B)", callback_data='model_fast')],
            [InlineKeyboardButton("⚖️ Balanced (70B)", callback_data='model_balanced')],
            [InlineKeyboardButton("💪 Powerful (405B)", callback_data='model_powerful')]
        ]
        
        text = f"""🤖 **Model Selection**

Current: {current}

⚡ Fast - Quick responses
⚖️ Balanced - Default
💪 Powerful - Best quality

Choose:"""
        
        if update.message:
            await update.message.reply_text(
                text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif update.callback_query:
            await update.callback_query.message.reply_text(
                text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    except Exception as e:
        logger.error(f"Model error: {e}")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats"""
    try:
        uptime = str(timedelta(seconds=int(time.time() - bot_stats["start_time"])))
        
        text = f"""📊 **Statistics**

⏱️ Uptime: {uptime}
👥 Users: {len(bot_stats['total_users'])}
💬 Messages: {bot_stats['total_messages']}
🧠 Active: {len(user_conversations)}
❌ Errors: {bot_stats['errors']}

🚀 Version: 1.1.0
⚡ Status: Online"""
        
        if update.message:
            await update.message.reply_text(text, parse_mode='Markdown')
        elif update.callback_query:
            await update.callback_query.message.reply_text(text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Stats error: {e}")

# ==================== MESSAGE HANDLER ====================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages"""
    try:
        user_id = update.effective_user.id
        user_message = update.message.text
        
        bot_stats["total_users"].add(user_id)
        bot_stats["total_messages"] += 1
        
        logger.info(f"User {user_id}: {user_message[:30]}...")
        
        await update.message.chat.send_action(action="typing")
        
        ai_response = get_ai_response(user_id, user_message)
        
        await update.message.reply_text(ai_response)
        
        logger.info(f"Bot replied to {user_id}")
    except Exception as e:
        logger.error(f"Message error: {e}")
        try:
            await update.message.reply_text("❌ Error occurred. Try again!")
        except:
            pass

# ==================== CALLBACK HANDLER ====================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    try:
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        data = query.data
        
        if data == 'chat':
            await query.message.reply_text("💬 Send me a message!")
        
        elif data == 'help':
            await help_command(update, context)
        
        elif data == 'models':
            await model_command(update, context)
        
        elif data == 'stats':
            await stats_command(update, context)
        
        elif data.startswith('model_'):
            model_type = data.split('_')[1]
            user_models[user_id] = MODELS[model_type]
            await query.message.reply_text(
                f"✅ Model changed to {MODELS[model_type]}!"
            )
    except Exception as e:
        logger.error(f"Callback error: {e}")

# ==================== ERROR HANDLER ====================

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Global error handler"""
    logger.error(f"Update {update} caused error: {context.error}")
    bot_stats["errors"] += 1

# ==================== MAIN ====================

def main():
    """Main function"""
    if not TELEGRAM_TOKEN:
        logger.error("❌ No TELEGRAM_BOT_TOKEN!")
        return
    
    if not SAMBANOVA_API_KEY:
        logger.error("❌ No SAMBANOVA_API_KEY!")
        return
    
    logger.info("✨ Starting bot...")
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("reset", reset_command))
    app.add_handler(CommandHandler("model", model_command))
    app.add_handler(CommandHandler("stats", stats_command))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Buttons
    app.add_handler(CallbackQueryHandler(button_callback))
    
    # Errors
    app.add_error_handler(error_handler)
    
    logger.info("🚀 Bot running!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()