# Telegram Error Reporter

A lightweight Python utility that sends real-time error notifications to a Telegram channel. Great for long-running scripts, cron jobs, or microservices needing instant error visibility.

---

## Features

- Real-time error alerts to Telegram
- Includes detailed traceback for debugging
- Markdown-formatted messages
- Minimal dependencies (`requests`, `python-dotenv`)
- Easy plug-and-play with any Python project

---

## Prerequisites

- Python 3.7+
- [Telegram Bot Token](https://t.me/BotFather) (create with @BotFather)
- Telegram Channel where the bot is added as an **admin**
- Telegram Channel ID:
  - For **public**: `@your_channel_username`
  - For **private**: use the numeric ID like `-1001234567890`

---

## Installation

```bash
pip install requests python-dotenv
```

---

## Configuration

Create a .env file in your project root and add your bot credentials:

```
TELEGRAM_BOT_TOKEN=123456789:ABCdefYourBotTokenHere
TELEGRAM_CHANNEL_ID=@your_channel_username
```

---

## Future Enhancements

- Error Grouping
  -  Reduce noise by grouping repeated errors with matching stack traces.
- Rate Limiting
  -  Prevent spamming by limiting how often the same error is reported.
- Persistent Logging
  -  Store error events in SQLite, PostgreSQL, or flat files.
- Web Dashboard
  -  Build a Flask or FastAPI frontend to browse, search, and manage error logs.
- Multi-Channel Alerts
  -  Expand support for Slack, Discord, SMS, or email notifications.
- Authentication
  -  Add API key protection for third-party error posting.
- Context Replay
  -  Log request/response pairs for easier bug reproduction.
- CI/Git Metadata
  -  Attach commit hashes, branch names, or deployment IDs to errors.
