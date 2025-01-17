import pandas as pd
import os
import sqlite3


class ExcelHandler:
    def __init__(self, excel_path):
        self.excel_path = excel_path
    
    def read_clients(self):
        try:
            if not os.path.exists(self.excel_path):
                print(f"File not found at: {self.excel_path}")
                return []
            
            print(f"Reading file from: {self.excel_path}")
            file_extension = os.path.splitext(self.excel_path)[1].lower()
            
            if file_extension == '.csv':
                df = pd.read_csv(self.excel_path, sep='\t') 
            elif file_extension == '.xlsx':
                df = pd.read_excel(self.excel_path, engine='openpyxl')
            elif file_extension == '.xls':
                df = pd.read_excel(self.excel_path, engine='xlrd')
            else:
                print(f"Unsupported file extension: {file_extension}")
                return []
            
            print(f"Available columns in file: {df.columns.tolist()}")
            
            if not all(col in df.columns for col in ['emails', 'company_name']):
                print("Required columns 'emails' and 'company_name' not found")
                print(f"Available columns: {df.columns.tolist()}")
                raise ValueError("File must contain 'emails' and 'company_name' columns")
            df = df.dropna(subset=['emails'])
            clients = df[['emails', 'company_name']].to_dict('records')
            print(f"Successfully read {len(clients)} clients from file")
            return clients
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            print(f"Full file path: {os.path.abspath(self.excel_path)}")
            return []

    def get_unsent_clients(self, db):
        print("Getting unsent clients...")
        all_clients = self.read_clients()
        if not all_clients:
            return []
            
        try:
            with sqlite3.connect(db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT recipient FROM sent_emails')
                sent_emails = {row[0] for row in cursor.fetchall()}
            
            unsent_clients = [client for client in all_clients if client['emails'] not in sent_emails]
            print(f"Found {len(unsent_clients)} unsent clients")
            return unsent_clients
        except sqlite3.Error as e:
            print(f"Database error: {str(e)}")
            return []
