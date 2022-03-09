import smtplib

class Mailer:

    smtp = None
    sender_email = None
    sender_name = None
    receivers = None
    subject = None
    body = None

    def __init__(self, host, port):
        try:
            self.smtp = smtplib.SMTP(host, port)
            print(f"INFO: connected to SMTP")
        except Exception as e:
            print(f"EXCEPTION: unable to connect to SMTP\n{e}")

    def build_message(self, sender_email, sender_name, receivers, subject, body):

        self.sender_email = sender_email
        self.sender_name = sender_name
        self.receivers = receivers
        self.subject = subject
        self.body = body
        self.message = f"From:{ sender_name } <{ sender_email }>\n"+ \
                       f"To:{ ' '.join(f'{receiver_name} <{receiver_email}>' for receiver_name, receiver_email in receivers) }\n"+ \
                       f"Subject:{ subject }\n"+ \
                       f"\n"+ \
                       f"{ body }"

    def send(self):
        try:
            self.smtp.sendmail(self.sender_email, [email for _, email in self.receivers], self.message)
            print(f"Successfully sent email")
        except Exception as e:
            print(f"EXCEPTION: unable to send email\n{e}")
