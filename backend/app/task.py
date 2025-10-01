from app.celery_app import celery_app
from twilio.rest import Client

# Twilio sandbox values
from_whatsapp = "whatsapp:+14155238886"  # Twilio sandbox number
account_sid = "AC6989cae13525a04e4d151f933ebff209"
auth_token = '[AuthToken]'  # Replace with your Twilio auth token

client = Client(account_sid, auth_token)

@celery_app.task
def send_whatsapp_reminder(to_number: str, message: str):
    """
    Send a WhatsApp message via Twilio sandbox.
    Example to_number: 'whatsapp:+91XXXXXXXXXX'
    """
    msg = client.messages.create(
        body=message,
        from_=from_whatsapp,
        to=to_number
    )
    return msg.sid