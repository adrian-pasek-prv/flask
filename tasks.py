import os
import requests
from dotenv import load_dotenv

# Because tasks.py is a seperate process we need to load enviroment variables 
# here also because create_app() function will not affect this file
load_dotenv()

DOMAIN = os.getenv('MAILGUN_DOMAIN')

def send_simple_message(to, subject, body):
    domain = os.getenv('MAILGUN_DOMAIN')
    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", os.getenv('MAILGUN_API_KEY')),
        data={"from": f"Adrian Pasek <mailgun@{domain}>",
            "to": [to],
            "subject": subject,
            "text": body})