from threading import Thread
from flask import current_app,render_template
from flask_mail import Message
from . import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, text_body, html_body):
    msg = Message(
        subject=subject,
        recipients=[recipients],
    )
    msg.body = text_body
    msg.html = html_body
    thr=Thread(target=send_async_email,
                args=(current_app._get_current_object(), msg))
        
    thr.start()
