import os
from dotenv import load_dotenv
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
print(f"SMTP_SERVER: {os.getenv('SMTP_SERVER')}")
print(f"SMTP_PORT: {os.getenv('SMTP_PORT')}")
print(f"SMTP_USERNAME: {os.getenv('SMTP_USERNAME')}")

SMTP_SERVER = os.getenv('SMTP_SERVER', )
SMTP_PORT = 465  # Using your SSL port directly
SMTP_USERNAME = os.getenv('SMTP_USERNAME', )
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
EXCEL_PATH = os.getenv('EXCEL_PATH', str(BASE_DIR / 'emails.xlsx'))
DB_PATH = os.getenv('DB_PATH', str(BASE_DIR / 'database' / 'database.sqlite'))