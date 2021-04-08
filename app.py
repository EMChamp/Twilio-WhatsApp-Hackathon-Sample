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
    message_body_received = request.form['Body']
    response = MessagingResponse()
    message = Message()
    message.body('Message Received! Your message was: ' + message_body_received)
    response.append(message)
    return str(response)

@app.route('/received_message_studio', methods=['POST'])
def response_received_message():
    print(request.form['Body'])
    client = Client(account_sid, auth_token)
    from_number = request.form['From'][9:] #Skip 'whatsapp:'
    client.studio \
        .flows('FWf8738d1bc2048114b99e2da6d1bd392b') \
        .executions \
        .create(to=from_number, from_='+14083009148')
    return {}

if __name__ == '__main__':
    app.run()