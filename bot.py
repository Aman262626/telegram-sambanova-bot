#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot with SambaNova AI
Multi-language support: English, Hindi, Hinglish
"""

import os
import logging
import requests
from datetime import datetime, timedelta
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

# Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SAMBANOVA_API_KEY = os.getenv("SAMBANOVA_API_KEY")
SAMBANOVA_URL = "https://api.sambanova.ai/v1/chat/completions"
DEFAULT_MODEL = "Meta-Llama-3.1-70B-Instruct"

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Storage
user_conversations = {}  # Store conversation history
user_models = {}  # Store user's preferred model
bot_stats = {
    "start_time": time.time(),
    "total_messages": 0,
    "total_users": set(),
    "errors": 0
}

# Available models
MODELS = {
    "fast": "Meta-Llama-3.1-8B-Instruct",
    "balanced": "Meta-Llama-3.1-70B-Instruct",
    "powerful": "Meta-Llama-3.1-405B-Instruct"
}

def get_ai_response(user_id: int, message: str) -> str:
    """Get AI response from SambaNova API"""
    try:
        # Initialize user data
        if user_id not in user_conversations:
            user_conversations[user_id] = []
        
        if user_id not in user_models:
            user_models[user_id] = DEFAULT_MODEL
        
        # Add user message
        user_conversations[user_id].append({
            "role": "user",
            "content": message
        })
        
        # Keep last 20 messages for memory optimization
        if len(user_conversations[user_id]) > 20:
            user_conversations[user_id] = user_conversations[user_id][-20:]
        
        # System prompt
        system_prompt = {
            "role": "system",
            "content": """You are a friendly and helpful AI assistant.
            
Supported Languages:
- English
- Hindi (हिंदी)
- Hinglish (Hindi + English mix)

Capabilities:
- Answer questions on any topic
- Help with coding and programming
- Creative writing and content generation
- Explain complex concepts simply
- Have natural conversations

Be conversational, helpful, and concise. Detect the user's language and respond accordingly."""
        }
        
        # Prepare API request
        headers = {
            "Authorization": f"Bearer {SAMBANOVA_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": user_models[user_id],
            "messages": [system_prompt] + user_conversations[user_id],
            "temperature": 0.7,
            "max_tokens": 1500
        }
        
        # Call API
        response = requests.post(
            SAMBANOVA_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            ai_message = response.json()['choices'][0]['message']['content']
            
            # Add AI response to history
            user_conversations[user_id].append({
                "role": "assistant",
                "content": ai_message
            })
            
            return ai_message
        else:
            bot_stats["errors"] += 1
            logger.error(f"API Error: {response.status_code} - {response.text}")
            return f"⚠️ Sorry, API returned error {response.status_code}. Please try again!"
    
    except requests.exceptions.Timeout:
        bot_stats["errors"] += 1
        return "⏱️ Request timeout! API took too long to respond. Please try again."
    
    except Exception as e:
        bot_stats["errors"] += 1
        logger.error(f"Error in get_ai_response: {e}")
        return f"❌ Error: {str(e)}\n\nPlease try again or contact admin."

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user_name = update.effective_user.first_name
    
    keyboard = [
        [
            InlineKeyboardButton("💬 Start Chat", callback_data='chat'),
            InlineKeyboardButton("ℹ️ Help", callback_data='help')
        ],
        [
            InlineKeyboardButton("🤖 Change Model", callback_data='models'),
            InlineKeyboardButton("📊 Stats", callback_data='stats')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""👋 **Namaste {user_name}!**

🤖 I'm an AI-powered bot using **SambaNova** technology!

**What I can do:**
✅ Answer questions in English/Hindi/Hinglish
✅ Help with coding & programming
✅ Creative writing & content
✅ Explain complex topics
✅ Have natural conversations

**Quick Start:**
Just send me any message to start chatting!

**Commands:**
/help - Show all commands
/reset - Clear conversation
/model - Change AI model
/stats - View bot statistics

Powered by 🚀 SambaNova AI"""
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """🆘 **Help Menu**

**Available Commands:**
/start - Start the bot
/help - Show this help menu
/reset - Clear conversation history
/model - Change AI model
/stats - View bot statistics

**How to Use:**
Simply send any message and I'll respond!

**Examples:**
• "What is quantum computing?"
• "Write a Python function to sort a list"
• "Mujhe AI ke baare mein batao"
• "Tell me a joke"
• "Coding kaise seekhein?"

**Supported Languages:**
🇬🇧 English
🇮🇳 Hindi (हिंदी)
🔄 Hinglish (Mix)

**Features:**
• Conversation memory (last 10 exchanges)
• Multiple AI models
• Fast responses
• 24/7 availability

Enjoy chatting! 🚀"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def reset_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /reset command"""
    user_id = update.effective_user.id
    
    if user_id in user_conversations:
        msg_count = len(user_conversations[user_id])
        del user_conversations[user_id]
        await update.message.reply_text(
            f"✅ **Conversation Reset!**\n\nCleared {msg_count} messages. Starting fresh!",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            "💭 No conversation history found. Start chatting!"
        )

async def change_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /model command"""
    user_id = update.effective_user.id
    current_model = user_models.get(user_id, DEFAULT_MODEL)
    
    keyboard = [
        [InlineKeyboardButton("⚡ Fast (8B)", callback_data='model_fast')],
        [InlineKeyboardButton("⚖️ Balanced (70B) - Default", callback_data='model_balanced')],
        [InlineKeyboardButton("💪 Powerful (405B)", callback_data='model_powerful')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    model_text = f"""🤖 **AI Model Selection**

**Current Model:** {current_model}

**Available Models:**

⚡ **Fast (8B)**
- Quick responses
- Good for simple tasks
- Lower resource usage

⚖️ **Balanced (70B)** ⭐ Default
- Best performance/speed ratio
- Handles complex queries
- Recommended for most users

💪 **Powerful (405B)**
- Highest quality responses
- Best for complex tasks
- Slower but very accurate

Choose your preferred model:"""
    
    await update.message.reply_text(
        model_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    uptime = time.time() - bot_stats["start_time"]
    uptime_str = str(timedelta(seconds=int(uptime)))
    
    stats_text = f"""📊 **Bot Statistics**

⏱️ **Uptime:** {uptime_str}
👥 **Total Users:** {len(bot_stats['total_users'])}
💬 **Messages Processed:** {bot_stats['total_messages']}
🧠 **Active Conversations:** {len(user_conversations)}
❌ **Errors:** {bot_stats['errors']}

🚀 **Bot Version:** 1.0.0
🤖 **AI Provider:** SambaNova
⚡ **Status:** Operational

Thank you for using the bot! 🙏"""
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')

# Message Handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    user_message = update.message.text
    
    # Update stats
    bot_stats["total_users"].add(user_id)
    bot_stats["total_messages"] += 1
    
    logger.info(f"User {user_name} ({user_id}): {user_message[:50]}...")
    
    # Show typing indicator
    await update.message.chat.send_action(action="typing")
    
    # Get AI response
    ai_response = get_ai_response(user_id, user_message)
    
    # Send response
    await update.message.reply_text(ai_response)
    
    logger.info(f"Bot replied to {user_name}")

# Callback Query Handler
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if query.data == 'chat':
        await query.message.reply_text(
            "💬 **Let's chat!** Send me any message to start."
        )
    
    elif query.data == 'help':
        await help_command(update, context)
    
    elif query.data == 'models':
        await change_model(update, context)
    
    elif query.data == 'stats':
        await stats_command(update, context)
    
    elif query.data.startswith('model_'):
        model_type = query.data.split('_')[1]
        user_models[user_id] = MODELS[model_type]
        
        await query.message.reply_text(
            f"✅ **Model changed to:** {MODELS[model_type]}\n\nStart chatting with the new model!"
        )

# Error Handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    bot_stats["errors"] += 1
    
    if update and update.message:
        await update.message.reply_text(
            "❌ **Oops! Something went wrong.**\n\nPlease try again or use /help for assistance."
        )

def main():
    """Start the bot"""
    # Validate tokens
    if not TELEGRAM_TOKEN:
        logger.error("❌ TELEGRAM_BOT_TOKEN not found! Set it in environment variables.")
        return
    
    if not SAMBANOVA_API_KEY:
        logger.error("❌ SAMBANOVA_API_KEY not found! Set it in environment variables.")
        return
    
    logger.info("✨ Starting Telegram Bot with SambaNova AI...")
    
    # Create application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("reset", reset_conversation))
    application.add_handler(CommandHandler("model", change_model))
    application.add_handler(CommandHandler("stats", stats_command))
    
    # Add message handler
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    
    # Add callback query handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start polling
    logger.info("🚀 Bot is now running! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()