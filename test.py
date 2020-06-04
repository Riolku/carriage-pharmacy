import main

from flask_mail import Message

m = main.pharmacy.mail

app = main.pharmacy.app

print(app.config)

with app.app_context():
    msg = Message("abc", recipients = ["keenan@thegugelers.ca"])

    m.send(msg)
