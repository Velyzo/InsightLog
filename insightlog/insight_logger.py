import logging
import datetime
import os
import time
import platform
import psutil
import threading
import itertools
import json
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from logging.handlers import RotatingFileHandler
from termcolor import colored
from tabulate import tabulate
from functools import wraps

# Ensure Insight Folder Creation
def ensure_insight_folder():
    insight_dir = os.path.join(os.getcwd(), '.insight')
    os.makedirs(insight_dir, exist_ok=True)
    return insight_dir

# Logger Initialization with Rotating File Handler
def start_logging(name, save_log=True, log_dir=".insight", log_filename="app.log", max_bytes=1_000_000, backup_count=1, log_level=logging.DEBUG):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(log_level)
        
        if save_log:
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, log_filename)
            file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
            file_handler.setLevel(log_level)
            file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    return logger

# InsightLogger Class
class InsightLogger:
    def __init__(self, name, log_dir=".insight", log_filename="app.log"):
        self.logger = start_logging(name, log_dir=log_dir, log_filename=log_filename)
        self.insight_dir = ensure_insight_folder()
        self.error_count = defaultdict(int)
        self.execution_times = defaultdict(list)
        self.start_time = datetime.datetime.now()
        self.logs = []

    def log_function_time(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            spinner = itertools.cycle(['-', '/', '|', '\\'])
            
            def spin():
                while not self._stop_spin:
                    elapsed_time = (time.perf_counter() - start_time) * 1000
                    cpu_usage = psutil.cpu_percent()
                    mem_usage = psutil.virtual_memory().percent
                    print(f"\r{colored(next(spinner) + ' Processing...', 'cyan', attrs=['bold'])} {elapsed_time:.2f} ms | CPU: {cpu_usage}% | RAM: {mem_usage}%", end="")
                    time.sleep(0.1)
            
            self._stop_spin = False
            spin_thread = threading.Thread(target=spin, daemon=True)
            spin_thread.start()
            
            result = func(*args, **kwargs)
            
            self._stop_spin = True
            elapsed_time = (time.perf_counter() - start_time) * 1000
            print(f"\r{colored(f'✔️ {func.__name__} executed in {elapsed_time:.2f} ms.', 'green', attrs=['bold'])}")
            
            self.logger.info(f"Function '{func.__name__}' executed in {elapsed_time:.2f} ms.")
            self.execution_times[func.__name__].append(elapsed_time)
            return result
        return wrapper
    
    def log_message(self, level, message):
        self.error_count[level] += 1
        log_entry = {"timestamp": datetime.datetime.now().isoformat(), "level": level, "message": message}
        self.logs.append(log_entry)
        with open(os.path.join(self.insight_dir, 'logs.json'), 'w') as f:
            json.dump(self.logs, f, indent=4)
        self.logger.log(getattr(logging, level.upper(), logging.INFO), message)
    
    def generate_insights(self):
        environment_info = {
            "Python Version": platform.python_version(),
            "Operating System": platform.system(),
            "OS Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "CPU Cores": psutil.cpu_count(),
            "Memory": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            "Uptime (s)": (datetime.datetime.now() - self.start_time).total_seconds()
        }
        
        summary = tabulate(environment_info.items(), headers=["Metric", "Value"], tablefmt="fancy_grid")
        print(summary)
        
        levels, counts = zip(*self.error_count.items()) if self.error_count else ([], [])
        if levels:
            plt.bar(levels, counts, color='skyblue', edgecolor='black')
            plt.xlabel('Log Level')
            plt.ylabel('Count')
            plt.title('Log Level Distribution')
            plt.xticks(rotation=45)
            plt.savefig(os.path.join(self.insight_dir, 'log_distribution.png'))
            plt.close()
            self.logger.info("Log distribution graph saved.")
    
# Example Usage
def main():
    try:
        insight_logger = InsightLogger("InsightLog")
        
        @insight_logger.log_function_time
        def example_function():
            time.sleep(1.5)
        
        example_function()
        
        insight_logger.log_message("INFO", "This is an info log.")
        insight_logger.log_message("ERROR", "This is an error log.")
        insight_logger.log_message("SUCCESS", "This is a success log.")
        insight_logger.log_message("WARNING", "This is a warning log.")
        insight_logger.log_message("DEBUG", "This is a debug log.")
        insight_logger.log_message("CRITICAL", "This is a critical log.")
        
        insight_logger.generate_insights()
    
    except Exception as e:
        print(colored(f"💥 Error: {e}", "red", attrs=["bold"]))

if __name__ == "__main__":
    main()