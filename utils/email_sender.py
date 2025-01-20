import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD
import random
import time
from email.utils import formatdate
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class EmailSender:
    def __init__(self):
        self.server = None
        self.connected = False
        self.email_queue = []
        self.last_sent_time = None
        self.consecutive_failures = 0
        self.max_retries = 3
        self.min_delay_between_sends = 300  # 5 minutes

    def connect(self):
        """Establish connection to SMTP server with retry logic"""
        retries = 0
        while retries < self.max_retries and not self.connected:
            try:
                print("Attempting to connect to the SMTP server using SSL...")
                self.server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
                self.server.login(SMTP_USERNAME, SMTP_PASSWORD)
                self.connected = True
                print("Connection to the SMTP server established successfully.")
                return True
            except smtplib.SMTPException as e:
                retries += 1
                print(f"Connection attempt {retries} failed: {e}")
                if retries < self.max_retries:
                    print(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    print("Max retries reached. Could not establish connection.")
                    return False

    def ensure_connection(self):
        if not self.connected or self.server is None:
            return self.connect()
        try:
            self.server.noop()
            return True
        except:
            print("Connection lost. Attempting to reconnect...")
            self.connected = False
            self.server = None
            return self.connect()

    def disconnect(self):
        if self.server and self.connected:
            try:
                self.server.quit()
                print("Disconnected from the SMTP server.")
            except smtplib.SMTPException as e:
                print(f"Failed to disconnect cleanly: {e}")
            finally:
                self.connected = False
                self.server = None

    def set_email_queue(self, emails):
        self.queue = emails

    
    def send_email(self, recipient, subject, body, company_name, next_email_info=None):
        """Send email with improved anti-blocking measures"""
        if self.last_sent_time:
            time_since_last = (datetime.now() - self.last_sent_time).total_seconds()
            if time_since_last < self.min_delay_between_sends:
                wait_time = self.min_delay_between_sends - time_since_last
                print(f"Waiting {wait_time:.0f} seconds before sending next email...")
                time.sleep(wait_time)

        for attempt in range(self.max_retries):
            if attempt > 0:
                wait_time = (2 ** attempt) * 60  
                print(f"Retry attempt {attempt + 1}, waiting {wait_time} seconds...")
                time.sleep(wait_time)

            if not self.ensure_connection():
                print(f"Failed to send email to {recipient}: Could not establish connection")
                continue

            try:
                print(f"Sending email to: {recipient} (Company: {company_name})")
                
                body = body.format(company_name=company_name)
                msg = MIMEMultipart('alternative')
                msg['From'] = f"Deutics Global <{SMTP_USERNAME}>"
                msg['To'] = recipient
                msg['Subject'] = subject
                msg['Message-ID'] = f"<{int(time.time())}@deutics.com>"
                msg['Date'] = formatdate(localtime=True)

                text_content = BeautifulSoup(body, 'html.parser').get_text()
                msg.attach(MIMEText(text_content, 'plain'))
                msg.attach(MIMEText(body, 'html'))
                
                self.server.send_message(msg)
                print(f"Email sent to {recipient} successfully.")
                self.consecutive_failures = 0
                self.last_sent_time = datetime.now()

                if next_email_info:
                    print("\nNext upcoming email:")
                    print(f"→ Recipient: {next_email_info['email']}")
                    print(f"→ Company: {next_email_info['company_name']}")
                    print(f"→ Will be sent at: {next_email_info['send_time'].strftime('%H:%M:%S')}")
                    # print(f"\nWaiting until {next_email_info['send_time'].strftime('%H:%M:%S')} to send next email...")
                
                return True

            except smtplib.SMTPException as e:
                print(f"Failed to send email to {recipient}: {e}")
                self.connected = False
                self.server = None
                self.consecutive_failures += 1
                
                # If we've failed too many times, take a longer break
                if self.consecutive_failures >= 3:
                    cooldown = 3600  # 1 hour cooldown
                    print(f"Too many consecutive failures. Taking a {cooldown/3600} hour break...")
                    time.sleep(cooldown)
                    self.consecutive_failures = 0
                    
            except Exception as e:
                print(f"Unexpected error while sending email to {recipient}: {e}")
                self.consecutive_failures += 1

        return False