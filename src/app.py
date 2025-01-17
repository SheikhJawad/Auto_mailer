# from database.db import EmailDatabase
# from utils.excel_handler import ExcelHandler
# from utils.email_sender import EmailSender
# from utils.file_watcher import start_file_watcher
# from config.settings import DB_PATH, EXCEL_PATH
# from templates.email_templates import * 
# import time
# import random

# class EmailAutomation:
#     def __init__(self):
#         self.db = EmailDatabase(DB_PATH)
#         self.excel_handler = ExcelHandler(EXCEL_PATH)
#         self.email_sender = EmailSender()
        
#     def get_random_template(self):
#         if EMAIL_TEMPLATES:
#             template = random.choice(EMAIL_TEMPLATES)
#             return template.get('subject', ''), template.get('body', '')
#         return None, None
        
#     def process_new_clients(self):
#         print("Processing new clients...")
#         unsent_clients = self.excel_handler.get_unsent_clients(self.db)

#         if unsent_clients:
#             print(f"Found {len(unsent_clients)} new clients to process")
#             self.email_sender.connect()
#             try:
#                 for client in unsent_clients:
#                     subject, body = self.get_random_template()
#                     if subject and body:
#                         company_name = client.get('company_name', 'Valued Client')  # Get company name for email
#                         print(f"Sending email to: {client['emails']} (Company: {company_name})")
                        
#                         self.email_sender.send_email(
#                             client['emails'],
#                             subject,
#                             body,
#                             company_name  # Pass company name here
#                         )
#                         self.db.record_sent_email(client['emails'], 0)  

        
#                         delay = random.randint(30, 90)
#                         print(f"Waiting {delay} seconds before next email...")
#                         time.sleep(delay)
#                     else:
#                         print("No email template available")
#             except Exception as e:
#                 print(f"Error processing clients: {str(e)}")
#             finally:
#                 self.email_sender.disconnect()
#         else:
#             print("No new clients to process")

            
#     def run(self):
#         observer = start_file_watcher(EXCEL_PATH, self.process_new_clients)
#         try:
#             while True:
#                 self.process_new_clients()
#                 delay = random.randint(1800, 3600)
#                 print(f"Waiting for next check cycle ({delay/60:.1f} minutes)...")
#                 time.sleep(delay)
#         except KeyboardInterrupt:
#             observer.stop()
#         observer.join()
from database.db import EmailDatabase
from utils.excel_handler import ExcelHandler
from utils.email_sender import EmailSender
from utils.file_watcher import start_file_watcher
from config.settings import DB_PATH, EXCEL_PATH
from templates.email_templates import *
import time
import random
from datetime import datetime, timedelta

class EmailAutomation:
    def __init__(self):
        self.db = EmailDatabase(DB_PATH)
        self.excel_handler = ExcelHandler(EXCEL_PATH)
        self.email_sender = EmailSender()
        self.processing = False
        self.min_delay_between_emails = 300  # 5 minutes
        self.max_delay_between_emails = 900  # 15 minutes
        self.check_interval = (3600, 7200)  # Check every 1-2 hours
        self.emails_per_batch = 10  # Process 10 emails at a time
        self.batch_cooldown = 7200  # 2 hours between batches

    def prepare_email_queue(self, unsent_clients):
        email_queue = []
        current_time = datetime.now()
        
        clients_to_process = unsent_clients[:self.emails_per_batch]
        
        for client in clients_to_process:
            delay = random.randint(self.min_delay_between_emails, self.max_delay_between_emails)
            send_time = current_time + timedelta(seconds=delay)
            subject, body = self.get_random_template()
            
            if subject and body:
                email_queue.append({
                    'email': client['emails'],
                    'company_name': client.get('company_name', 'Valued Client'),
                    'subject': subject,
                    'body': body,
                    'send_time': send_time
                })
                current_time = send_time
                
        return email_queue
        
    def get_random_template(self):
        if EMAIL_TEMPLATES:
            template = random.choice(EMAIL_TEMPLATES)
            return template.get('subject', ''), template.get('body', '')
        return None, None


    def process_new_clients(self):
        if self.processing:
            print("Already processing clients. Skipping this cycle.")
            return

        try:
            self.processing = True
            print("Processing new clients...")
            unsent_clients = self.excel_handler.get_unsent_clients(self.db)

            if not unsent_clients:
                print("No new clients to process")
                return

            print(f"Found {len(unsent_clients)} new clients to process")
            email_queue = self.prepare_email_queue(unsent_clients)
            self.email_sender.set_email_queue(email_queue)

            for i, email in enumerate(email_queue):
                current_time = datetime.now()
                wait_time = (email['send_time'] - current_time).total_seconds()
                
                if wait_time > 0:
                    print(f"\nWaiting until {email['send_time'].strftime('%H:%M:%S')} to send next email...")
                    time.sleep(wait_time)

                # Prepare next email info if available
                next_email_info = None
                if i < len(email_queue) - 1:
                    next_email_info = email_queue[i + 1]

                success = self.email_sender.send_email(
                    recipient=email['email'],
                    subject=email['subject'],
                    body=email['body'],
                    company_name=email['company_name'],
                    next_email_info=next_email_info
                )

                if success:
                    self.db.record_sent_email(email['email'], 0)
                else:
                    print(f"Failed to send email to {email['email']}, will retry in next cycle")

        except Exception as e:
            print(f"Error in process_new_clients: {str(e)}")
        finally:
            self.processing = False
            self.email_sender.disconnect()

    def run(self):
        print("Starting Email Automation System...")
        observer = start_file_watcher(EXCEL_PATH, self.process_new_clients)
        
        try:
            while True:
                try:
                    self.process_new_clients()
                except Exception as e:
                    print(f"Error during processing cycle: {str(e)}")
                
                delay = random.randint(*self.check_interval)
                print(f"\nWaiting for next check cycle ({delay/60:.1f} minutes)...")
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print("\nShutting down gracefully...")
            observer.stop()
            self.email_sender.disconnect()
        
        observer.join()

