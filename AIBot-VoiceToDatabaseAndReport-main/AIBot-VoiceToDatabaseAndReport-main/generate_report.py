import json
import re
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create an OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Defining the schema that the AI should fill when parsing transcripts
# Ensures consistent data structure in JSON output
schema = {
    "agent_name": "",
    "client_name": "",
    "appointment_happened": None,
    "agreement_signed": None,
    "showings_scheduled": [],
    "price_point": {"min": None, "max": None},
    "lender_application_submitted": None,
    "lender_app_reason_not_submitted": "",
    "not_signed_reason": "",
    "future_openness": "",
    "financially_viable": None,
    "all_decision_makers_present": None,
    "follow_up_appointment": {"date": "", "location": ""},
    "free_notes": ""
}

# System prompt for the AI: tells the model exactly how to respond - For future use
system_prompt = f"""
You are an AI real estate assistant. 
Given an agent's transcript, extract all fields exactly as in this JSON schema: {json.dumps(schema, indent=2)}.
- Return JSON only, nothing else.
- If any information is missing, set booleans to null and strings to "".
- Detect the agent's name and the client's name from the transcript if possible.
- For financially_viable, return True, False, or "Unknown".
"""

def generate_report(transcript: str, fallback_agent_name: str = "") -> dict:
    """
    Given a transcript of a conversation between a real estate agent and client:
    - Ask the OpenAI API to extract structured information into the schema
    - Provide fallback handling if parsing fails
    - Return both JSON data and a human-readable text report
    """

    # Send transcript to OpenAI with the system instructions
    response = client.chat.completions.create(
        model="gpt-5",  # specify the model
        messages=[
            # System message: sets the behavior, rules, and formatting requirements
            # The model must follow these instructions for the entire conversation
            {"role": "system", "content": system_prompt},
            # User message: the actual input (agent transcript) that the model will analyze
            # The model uses the transcript as the "data source" while following the system instructions
            {"role": "user", "content": transcript}
        ]
    )

    # Get the AI’s raw JSON output (as string)
    output_text = response.choices[0].message.content.strip()

    try:
        # Try to parse the AI's output into JSON
        json_output = json.loads(output_text)
    except Exception:
        # If parsing fails, fall back to the schema and store transcript as notes
        json_output = schema.copy()
        json_output["free_notes"] = transcript

    # If agent name was not detected, use the fallback value (if provided)
    if not json_output.get("agent_name") and fallback_agent_name:
        json_output["agent_name"] = fallback_agent_name

    # If client name was not detected, try regex search for a name in the transcript
    if not json_output.get("client_name"):
        match = re.search(r"with ([A-Z][a-z]+ [A-Z][a-z]+)", transcript)
        json_output["client_name"] = match.group(1) if match else "Unknown"

    # Generate a human-readable summary string
    text_report = generate_human_readable(json_output)

    # Return both the JSON schema data and the formatted summary
    return {"json_output": json_output, "text_report": text_report}


def generate_human_readable(data: dict) -> str:
    """
    Convert the structured JSON data into a nicely formatted text report
    that is easier to read for humans.
    """

    lines = [
        f"Agent: {data.get('agent_name', 'Unknown')}",
        f"Client: {data.get('client_name', 'Unknown')}",
        f"Appointment: {'Occurred' if data.get('appointment_happened') else 'Did not occur'}; Agreement signed: {data.get('agreement_signed')}"
    ]

    # List out property showings if any are scheduled
    if data.get("showings_scheduled"):
        lines.append("Showings:")
        for s in data["showings_scheduled"]:
            lines.append(f"  - {s}")

    # Format price point (budget range) if available
    price = data.get("price_point", {})
    if price.get("min") and price.get("max"):
        lines.append(f"Budget: ${price['min']:,}–${price['max']:,}")

    # Handle lender application status
    lender_submitted = data.get("lender_application_submitted")
    lender_reason = data.get("lender_app_reason_not_submitted")
    if lender_submitted is True:
        lines.append("Lender application: Submitted")
    elif lender_submitted is False:
        lines.append(f"Lender application: Not submitted; {lender_reason}")

    # Decision makers and future openness to working with the agent
    lines.append(f"Decision makers present: {data.get('all_decision_makers_present')}")
    lines.append(f"Future openness: {data.get('future_openness', 'Unknown')}")

    # Follow-up appointment details if available
    follow_up = data.get("follow_up_appointment", {})
    if follow_up.get("date"):
        location = follow_up.get("location", "Unknown")
        lines.append(f"Follow-up: {follow_up['date']} ({location})")

    # Free notes and financial viability status
    lines.append(f"Preferences / Free notes: {data.get('free_notes', '')}")
    lines.append(f"Financially viable: {data.get('financially_viable', 'Unknown')}")

    # Join everything into a single readable report string
    return "\n".join(lines)
