from flask import current_app, render_template
from flask_mail import Message
from app import mail, app
from threading import Thread


def send_async_mail(msg, app):
    with app.app_context():
        mail.send(msg)


def sent_token_to_email(user,token):
        msg = Message("From Flask app sent to you ",
                      sender=current_app.config['MAIL_USERNAME'],
                      recipients=[user.email], html=render_template('reset_password_mail.html', token=token, user=user))
        # mail.send(msg)
        Thread(target=send_async_mail, args=(msg, app)).start()
        #多线程, target是函数, args参数排序要与前面target函数参数顺序一致,