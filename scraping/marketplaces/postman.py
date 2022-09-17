from marketplaces.postman_info import email, password

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class Postman:

    def __init__(self, logger):
        self.logger = logger

    def send_logs(self):
        self.logger.zip_logs()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)

        message = MIMEMultipart()

        message['FROM'] = email
        message['TO'] = email
        message['SUBJECT'] = f'Parsed data for {self.logger.current_date}'

        with open(f'{self.logger.current_date}.zip', 'rb') as f:
            file = MIMEApplication(f.read(), 'zip')
        file.add_header('content-disposition', 'attachment', filename=f'{self.logger.current_date}.zip')
        message.attach(file)

        server.sendmail(email, email, message.as_string())

        self.logger.clear_logs()

