**AI Agent Follow-Up Bot**

The AI Agent Follow-Up Bot is a tool designed to help real estate agents streamline their reporting process.
It automatically transcribes voice notes, extracts structured client information, saves reports in a database, and sends summaries to a Telegram channel for easy access and sharing.

This reduces manual reporting time and ensures that important client details are never lost.


**Features**

Audio Transcription – Converts agent voice notes into text.

Structured Report Generation – Extracts key details such as:

Agent and client names

Appointment outcome

Agreement status

Scheduled showings

Budget / price point

Lender application details

Follow-up appointments

Free-form notes

Database Storage – Saves reports in a SQLite database for future access.

Telegram Integration – Automatically sends human-readable summaries to a Telegram channel.

File Management – Moves processed recordings into a “processed” folder to prevent duplication.


**Tech Stack**

Python 3.10+

OpenAI Whisper API – for transcription

OpenAI GPT Models – for structured report generation

SQLite – lightweight database for storing reports

Telegram Bot API – for instant report sharing


**Installation**

Clone the repository

git clone https://github.com/your-repo/ai-agent-bot.git
cd ai-agent-bot

Set up a virtual environment

python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows

Install dependencies

pip install -r requirements.txt

Set up environment variables
Create a .env file in the project root:

OPENAI_API_KEY=your_openai_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=your_telegram_channel_id


**Run the pipeline**

Place your .mp3 recordings into the agent_recordings folder, then run:

python pipeline.py


**Output**

Transcriptions appear in the console.

Structured reports are stored in agent_reports.db.

Telegram messages are sent automatically with a formatted summary.

Processed audio files are moved into the agent_recordings/processed folder.


**Next Steps**

Extend the bot into a fully conversational assistant that asks follow-up questions when information is missing.

Add multi-agent support for larger teams.

Build a dashboard for searching and exporting past reports.
