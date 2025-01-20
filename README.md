# Auto_mailer

An automated email marketing system built with Python for handling bulk email campaigns with customizable templates and tracking.

## Project Description

The Auto_mailer system automates email marketing campaigns with features including:
- Template-based email sending
- CSV-based recipient management
- Database tracking of sent emails
- Configurable SMTP settings
- File monitoring capabilities

## File Structure
```
Auto_mailer/
│
├── config/
│   └── settings.py           # Configuration and environment settings
│
├── utils/
│   ├── email_sender.py       # Email sending functionality
│   ├── file_watcher.py       # Monitors file changes
│   └── excel_handler.py      # Handles CSV processing
│
├── src/
│   └── app.py               # Core application logic
│
├── templates/
│   └── email_templates.py   # Email template definitions
│
├── emails/
│   └── emails.csv          # Recipient data
│
├── database/
│   └── db.py              # Database structure and operations
│
├── .env                    # Environment configuration
├── main.py                # Application entry point
└── requirements.txt       # Project dependencies
```

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/SheikhJawad/Auto_mailer.git
cd Auto_mailer
```

2. Create virtual environment:
```bash
python -m venv virtualenv
```

3. Activate virtual environment:
- Windows:
```bash
virtualenv\Scripts\activate
```
- Linux/Mac:
```bash
source virtualenv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create `.env` file with the following configuration:
```
SMTP_SERVER=
SMTP_PORT=
SMTP_USERNAME=y
SMTP_PASSWORD=your_password
EXCEL_PATH=path/to/emails.csv
DB_PATH=path/to/database.sqlite
```

6. Run the application:
```bash
python main.py
```

## Environment Configuration

Your `.env` file must include:
- SMTP server details (server, port)
- Authentication credentials (username, password)
- File paths (database, Excel file)

Example:
```
SMTP_SERVER=mail.gmail.com
SMTP_PORT=123
SMTP_USERNAME=xyz1@gmail.com
SMTP_PASSWORD=your_password
EXCEL_PATH= your excel file path in which you have all emails and company names
DB_PATH=your db sqlite file path
```

## Key Components

### settings.py
- Loads environment variables
- Configures SMTP settings
- Sets up database connection
- Manages file paths

### email_sender.py
- Handles email delivery
- Manages SMTP connections
- Processes email templates

### file_watcher.py
- Monitors CSV file changes
- Triggers updates on file modifications

### excel_handler.py
- Processes recipient data
- Validates email formats
- Manages CSV operations

### app.py
- Coordinates system components
- Implements business logic
- Manages email campaign flow

### db.py
- Defines database schema
- Handles email tracking
- Manages template storage

## Running the Project

1. Ensure virtual environment is activated
2. Verify `.env` configuration
3. Run the main application:
```bash
python main.py
```

The system will:
- Load configuration
- Connect to SMTP server
- Process recipient list
- Send emails based on templates
- Track delivery in database

## Dependencies
Required packages are listed in requirements.txt:
- python-dotenv
- pandas
- SQLite3
- Other required libraries

## Troubleshooting

Common issues:
1. SMTP Connection:
   - Verify credentials
   - Check port numbers
   - Confirm server address

2. File Paths:
   - Ensure correct paths in .env
   - Check file permissions
   - Verify file existence

3. Database:
   - Check SQLite file location
   - Verify table structure
   - Confirm write permissions

