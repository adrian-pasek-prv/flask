import os
import requests
from dotenv import load_dotenv
import jinja2

# Because tasks.py is a seperate process we need to load enviroment variables 
# here also because create_app() function will not affect this file
load_dotenv()

# load an HTML template with Jinja
template_loader = jinja2.FileSystemLoader('templates')
template_env = jinja2.Environment(loader=template_loader)

DOMAIN = os.getenv('MAILGUN_DOMAIN')

# Define render function that will locate template file
# and attach any keyword arguments within **context
# that can be later used as Jinja variables in html
def render_template(template_filename, **context):
    return template_env.get_template(template_filename).render(**context)

def send_simple_message(to, subject, body, html):
    domain = os.getenv('MAILGUN_DOMAIN')
    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", os.getenv('MAILGUN_API_KEY')),
        data={"from": f"Adrian Pasek <mailgun@{domain}>",
            "to": [to],
            "subject": subject,
            "text": body,
            "html": html})
    
def send_user_registration_email(email, username):
    return send_simple_message(
        email,
        "Successfully signed up",
        f'Hi {username}! You have successfully signed up to the Stores REST API',
        render_template('email/action.html', username=username)
    )