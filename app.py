from flask import Flask, request
from dotenv import load_dotenv
import os, pprint
pp = pprint.PrettyPrinter(indent=4)
app = Flask(__name__)
from twilio.rest import Client
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse

load_dotenv()
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

@app.route('/message_status_callback', methods=['POST'])
def message_status_callback():
    pp.pprint(request.form)
    return {}

@app.route('/incoming_message', methods=['POST'])
def incoming_message():
    pp.pprint(request.form)
    return {}

@app.route('/received_message_twiml', methods=['POST'])
def response_received_message_twiml():
    # Create TwiML objects
    response = MessagingResponse()
    message = Message()

    # Set Reply message
    message_body_received = request.form['Body']
    if "location" in message_body_received:
        message.body("Our office is located at 9 Straits View, Marina One.")
    elif "time" in message_body_received:
        message.body("Our office opens at 9AM and closes at 6PM.")
    elif "exit" in message_body_received:
        message.body("Goodbye!")
    else:
        message.body("Welcome to Twilio Singapore. \n"
                     "Please reply with the following words to get more information\n"
                     "- location\n"
                     "- time\n"
                     "- exit\n")

    response.append(message)

    # Response with TwiML
    return str(response)

@app.route('/received_message_studio', methods=['POST'])
def response_received_message():
    # Create Twilio Client
    client = Client(account_sid, auth_token)

    # Parse Message Body to Send to Studio
    message_body_received = request.form['Body']
    parameters = {'reply_message': message_body_received}

    # Set To/From numbers
    wa_sender_number = "whatsapp:" + request.form['From'][9:]
    whatsapp_sandbox_number = "whatsapp:+14155238886"

    # Execute studio flow w/ the Message Body as Parameter
    client.studio \
        .flows('FW4e0328e6706dec20203a525cf6c97144') \
        .executions \
        .create(to=wa_sender_number, from_=whatsapp_sandbox_number, parameters=parameters)
    return {}

if __name__ == '__main__':
    app.run()