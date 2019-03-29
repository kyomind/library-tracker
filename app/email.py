from threading import Thread
from flask import current_app,render_template
from flask_mail import Message
from . import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, template, **kwargs):
    msg = Message(
        subject=subject,
        recipients=[recipients],
    )
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr=Thread(target=send_async_email,
                args=(current_app._get_current_object(), msg))
        
    thr.start()
