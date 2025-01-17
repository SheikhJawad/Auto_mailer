from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class ExcelWatcher(FileSystemEventHandler):
    def __init__(self, excel_path, callback):
        self.excel_path = os.path.abspath(excel_path)  
        self.callback = callback
        
    def on_modified(self, event):

        if os.path.abspath(event.src_path) == self.excel_path:
            self.callback()

def start_file_watcher(excel_path, callback):

    watch_directory = os.path.dirname(excel_path)

    if not os.path.exists(watch_directory):
        os.makedirs(watch_directory, exist_ok=True)
    

    if not os.path.exists(excel_path):
        open(excel_path, 'a').close()
    
    event_handler = ExcelWatcher(excel_path, callback)
    observer = Observer()

    observer.schedule(event_handler, path=watch_directory, recursive=False)
    observer.start()
    return observer