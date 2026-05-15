from datetime import datetime
import os
LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs', 'pipeline.log')
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    
    with open(LOG_PATH, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
        