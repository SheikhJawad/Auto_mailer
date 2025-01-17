# import sqlite3
# from datetime import datetime

# class EmailDatabase:
#     def __init__(self, db_path):
#         self.db_path = db_path
#         self.init_db()

#     def init_db(self):
#         with sqlite3.connect(self.db_path) as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS email_templates (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     subject TEXT,
#                     body TEXT,
#                     created_at TIMESTAMP
#                 )
#             ''')
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS sent_emails (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     recipient TEXT,
#                     template_id INTEGER,
#                     sent_at TIMESTAMP,
#                     FOREIGN KEY (template_id) REFERENCES email_templates (id)
#                 )
#             ''')

#     def add_template(self, subject, body):
#         with sqlite3.connect(self.db_path) as conn:
#             cursor = conn.cursor()
#             cursor.execute(
#                 'INSERT INTO email_templates (subject, body, created_at) VALUES (?, ?, ?)',
#                 (subject, body, datetime.now())
#             )
#             return cursor.lastrowid

#     def get_random_template(self):
#         with sqlite3.connect(self.db_path) as conn:
#             cursor = conn.cursor()
#             cursor.execute('SELECT * FROM email_templates ORDER BY RANDOM() LIMIT 1')
#             return cursor.fetchone()

#     def record_sent_email(self, recipient, template_id):
#         with sqlite3.connect(self.db_path) as conn:
#             cursor = conn.cursor()
#             cursor.execute(
#                 'INSERT INTO sent_emails (recipient, template_id, sent_at) VALUES (?, ?, ?)',
#                 (recipient, template_id, datetime.now())
#             )
import sqlite3
from datetime import datetime

class EmailDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """
        Initialize the database with required tables if they don't exist.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS email_templates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject TEXT,
                    body TEXT,
                    created_at TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sent_emails (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipient TEXT,
                    template_id INTEGER,
                    sent_at TIMESTAMP,
                    FOREIGN KEY (template_id) REFERENCES email_templates (id)
                )
            ''')
            conn.commit()

    def add_template(self, subject, body):
        """
        Add a new email template to the database.
        Returns the ID of the newly created template.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO email_templates (subject, body, created_at) VALUES (?, ?, ?)',
                    (subject, body, datetime.now())
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding template: {e}")
            return None

    def get_random_template(self):
        """
        Get a random email template from the database.
        Returns a tuple containing template information or None if no templates exist.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM email_templates ORDER BY RANDOM() LIMIT 1')
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting random template: {e}")
            return None

    def record_sent_email(self, recipient, template_id):
        """
        Record a sent email in the database.
        Returns True if successful, False otherwise.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO sent_emails (recipient, template_id, sent_at) VALUES (?, ?, ?)',
                    (recipient, template_id, datetime.now())
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error recording sent email: {e}")
            return False

    def get_template_count(self):
        """
        Get the total number of templates in the database.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM email_templates')
                return cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Error getting template count: {e}")
            return 0

    def get_sent_emails(self):
        """
        Get all sent emails with their associated template information.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT se.*, et.subject, et.body 
                    FROM sent_emails se 
                    LEFT JOIN email_templates et ON se.template_id = et.id 
                    ORDER BY se.sent_at DESC
                ''')
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting sent emails: {e}")
            return []