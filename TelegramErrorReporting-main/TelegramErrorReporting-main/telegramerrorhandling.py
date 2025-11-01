# --- Imports ---

# Used to access environment variable file
import os

# Used to load variables from the `.env` file into environment variables
from dotenv import load_dotenv

# Used to send HTTP requests to the Telegram Bot API
import requests

# Used to capture and format the full errpr traceback (where and how the error occurred in code)
import traceback

# Used to generate a human-readable timestamp for when the error occurred
import datetime



# --- Load Environment Variables ---

# Loading evironment variables from a `.env` file so protect API keys from source code
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")


# --- Function: Send Message to Telegram ---

def send_telegram_message(message: str):

    # Telegram Bot API endpoint for sending messages
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # General term for data we're sending to an API. Formatted as a dictionary in Python, sent as a JSON in the bosy of a POST request
    # This payload structure is specific to the Telegram API for the method "sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,  # Who to send the message to
        "text": message,                 # What message to send
        "parse_mode": "Markdown"         # How to format it
    }

    # Make the HTTP POST request to send the message
    response = requests.post(url, json=payload)

    # Raise an error if the request failed (e.g., invalid token or wrong channel ID)
    response.raise_for_status()


# --- Function: Report an Error ---

def report_error(service: str, error: Exception):
    """
    Formats an error and sends it to Telegram.
    
    Args:
        service (str): The name of the service or module where the error occurred.
        error (Exception): The actual exception object.
    """
    # Get the current time for the error report
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Capture the full traceback as a string
    stack_trace = traceback.format_exc()

    # Build the formatted message using Markdown
    message = (
        f"🚨 *Error Alert* 🚨\n"
        f"*Service:* `{service}`\n"
        f"*Time:* `{now}`\n"
        f"*Error:* `{str(error)}`\n"
        f"```{stack_trace[-1500:]}```"  # Truncate if needed (Telegram has a character limit)
    )

    # Send the message using the bot
    send_telegram_message(message)


# --- Example Usage (For Testing) ---


# If this file is run dirrectly, __name__ will be "__main__". If this file is imported, __name__ will be the module name.
if __name__ == "__main__":
    # Simulate an error to test the reporting system
    try:
        # This will cause a ZeroDivisionError
        x = 1 / 0

    # "Exception" is the base class for built-in exceptions, so I'm giving the value as e
    except Exception as e:
        # Report the error to Telegram
        report_error("test-service", e)
