from pharmacy import mail_app

def send_mail(to_addr, subject, content):
  mail_app.send_message(Message(
    subject = subject,
    recipients = to_addr,
    html = content
  ))