from msilib.schema import MIME
import os
from shutil import make_archive

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class Postman:

    def __init__(self, logger):
        self.logger = logger

    def send_logs(self):
        self.logger.zip_logs()

        email = os.environ['MY_GMAIL']
        password = os.environ['CAR_ANALYSIS_GMAIL_PASSWORD']

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

