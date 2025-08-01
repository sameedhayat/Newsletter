import os, smtplib
from email.message import EmailMessage

class EmailSender:
    """
    Sends plain-text and HTML email using SMTP.
    """
    def __init__(self):
        self.host = os.getenv("SMTP_HOST")
        self.port = int(os.getenv("SMTP_PORT", 587))
        self.user = os.getenv("SMTP_USER")
        self.pass_ = os.getenv("SMTP_PASS")
        self.sender = os.getenv("EMAIL_SENDER")
        self.recipient = os.getenv("EMAIL_RECIPIENT")

    def send(self, subject: str, text: str, html: str):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"]    = self.sender
        msg["To"]      = self.recipient
        msg.set_content(text)
        msg.add_alternative(html, subtype='html')

        cls = smtplib.SMTP_SSL if self.port==465 else smtplib.SMTP
        with cls(self.host, self.port) as server:
            if self.port!=465:
                server.starttls()
            server.login(self.user, self.pass_)
            server.send_message(msg)