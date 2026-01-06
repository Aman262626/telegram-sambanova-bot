# 🤖 Telegram Bot with SambaNova AI

An intelligent Telegram bot powered by SambaNova's AI models with multi-language support (English, Hindi, Hinglish).

## ✨ Features

- 🤖 **AI-Powered Conversations** - Natural chat with advanced AI
- 🌍 **Multi-Language** - Supports English, Hindi, and Hinglish
- 🧠 **Conversation Memory** - Remembers context from previous messages
- ⚡ **Multiple Models** - Choose between Fast (8B), Balanced (70B), or Powerful (405B)
- 📊 **Statistics** - Track bot usage and performance
- 🔄 **Easy Reset** - Clear conversation history anytime
- 🛡️ **Error Handling** - Robust error management

## 🚀 Quick Start

### 1. Get Your Tokens

#### Telegram Bot Token:
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the token provided

#### SambaNova API Key:
1. Visit [SambaNova Cloud](https://sambanova.ai)
2. Sign up for an account
3. Generate an API key from dashboard
4. Copy the API key

### 2. Local Setup

```bash
# Clone repository
git clone https://github.com/Aman262626/telegram-sambanova-bot.git
cd telegram-sambanova-bot

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your tokens
nano .env

# Run bot
python bot.py
```

### 3. Deploy on Render (Free)

#### Step 1: Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

#### Step 2: Deploy on Render
1. Go to [render.com](https://render.com)
2. Sign up/Login
3. Click **New** → **Background Worker**
4. Connect your GitHub repository
5. Configure:
   - **Name**: `telegram-sambanova-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
6. Add Environment Variables:
   - `TELEGRAM_BOT_TOKEN`: Your bot token
   - `SAMBANOVA_API_KEY`: Your API key
7. Click **Create Background Worker**

✅ Your bot is now live 24/7!

## 📝 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and see welcome message |
| `/help` | Show help menu with all commands |
| `/reset` | Clear conversation history |
| `/model` | Change AI model (Fast/Balanced/Powerful) |
| `/stats` | View bot statistics |

## 🎯 Usage Examples

### English
```
User: What is artificial intelligence?
Bot: [Detailed explanation about AI]
```

### Hindi
```
User: मुझे coding सिखाओ
Bot: [कोडिंग सीखने के बारे में जानकारी]
```

### Hinglish
```
User: Python me function kaise banate hain?
Bot: [Explanation in Hinglish with code examples]
```

## 🤖 AI Models

| Model | Size | Speed | Use Case |
|-------|------|-------|----------|
| **Fast** | 8B | ⚡⚡⚡ | Quick queries, simple tasks |
| **Balanced** | 70B | ⚡⚡ | General use (default) |
| **Powerful** | 405B | ⚡ | Complex tasks, detailed responses |

## 🛠️ Configuration

### Environment Variables

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
SAMBANOVA_API_KEY=your_sambanova_api_key
```

### Conversation Memory

The bot stores the last **20 messages** (10 exchanges) per user for context. Older messages are automatically removed.

## 📊 Statistics

Track:
- ⏱️ Bot uptime
- 👥 Total users
- 💬 Messages processed
- 🧠 Active conversations
- ❌ Errors encountered

## 🔒 Security

- Never commit `.env` file to Git
- Keep API keys secret
- Use environment variables in production
- Regularly rotate API keys

## 🐛 Troubleshooting

### Bot not responding?
1. Check if bot token is correct
2. Verify SambaNova API key is valid
3. Check Render logs for errors
4. Ensure environment variables are set

### API errors?
1. Check SambaNova API quota
2. Verify API key permissions
3. Try a different model (smaller)

### Timeout errors?
1. Increase timeout in code (line ~120)
2. Use faster model (8B instead of 405B)
3. Check network connection

## 💻 Tech Stack

- **Language**: Python 3.11+
- **Framework**: python-telegram-bot 20.7
- **AI Provider**: SambaNova Cloud
- **Deployment**: Render (Free Tier)
- **Models**: Meta Llama 3.1 (8B/70B/405B)

## 📄 File Structure

```
telegram-sambanova-bot/
├── bot.py              # Main bot code
├── requirements.txt    # Python dependencies
├── Procfile            # Render deployment config
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📝 License

MIT License - Feel free to use for personal or commercial projects!

## 👤 Author

**Aman Kumar**
- GitHub: [@Aman262626](https://github.com/Aman262626)

## ⭐ Support

If you find this useful, please give it a star! ⭐

## 📧 Contact

For issues or questions:
- Open a GitHub issue
- Contact via Telegram: [@your_username]

---

**Built with ❤️ using SambaNova AI**

🚀 **Status**: Active Development
💫 **Version**: 1.0.0
⏱️ **Last Updated**: January 2026