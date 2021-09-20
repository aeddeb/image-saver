from flask import current_app
from flask_mail import Message
from flaskapp import mail
from flask import url_for

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                    sender = current_app.config['MAIL_USERNAME'],
                    recipients = [user.email])
    msg.body = f"""To reset your password, please visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, please ignore this email and no changes will be made.
"""
    mail.send(msg)