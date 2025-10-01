from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

# TWILIO_SID = os.getenv("TWILIO_SID")
# TWILIO_AUTH = os.getenv("TWILIO_AUTH")
# TWILIO_PHONE = os.getenv("TWILIO_PHONE")

TWILIO_SID = ""
TWILIO_AUTH = ""
TWILIO_PHONE = ""

client = Client(TWILIO_SID, TWILIO_AUTH)

def send_whatsapp_message(to_number: str, message: str):
    client.messages.create(
        from_=f"whatsapp:{TWILIO_PHONE}",
        body=message,
        to=f"whatsapp:{to_number}"
    )
