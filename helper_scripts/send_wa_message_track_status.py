import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load Account Sid/Auth Token
load_dotenv()
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

# Create Twilio Client
client = Client(account_sid, auth_token)
whatsapp_from_number = 'whatsapp:+14155238886'

# Send Message
message = client.messages.create(
                              from_= whatsapp_from_number,
                              body='Sent from send_wa_message.py',
                              to='whatsapp:+6597209504',
                              status_callback='https://rsunga01.ngrok.io/message_status_callback')