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
from collections import defaultdict
from logging.handlers import RotatingFileHandler
from termcolor import colored
from tabulate import tabulate
from functools import wraps

# Ensure Insight Folder Creation
def ensure_dir():
    dir_path = os.path.join(os.getcwd(), '.insight')
    os.makedirs(dir_path, exist_ok=True)
    return dir_path

# Logger Initialization
def init_log(name, save=True, dir=".insight", file="app.log", max_size=1_000_000, backups=1, level=logging.DEBUG):
    log = logging.getLogger(name)
    if not log.hasHandlers():
        log.setLevel(level)
        
        if save:
            os.makedirs(dir, exist_ok=True)
            path = os.path.join(dir, file)
            handler = RotatingFileHandler(path, maxBytes=max_size, backupCount=backups)
            handler.setLevel(level)
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            log.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setLevel(level)
        console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        log.addHandler(console)
    
    return log

# InsightLogger Class
class InsightLog:
    def __init__(self, name, dir=".insight", file="app.log"):
        self.log = init_log(name, dir=dir, file=file)
        self.dir = ensure_dir()
        self.errors = defaultdict(int)
        self.times = defaultdict(list)
        self.start = datetime.datetime.now()
        self.entries = self.load()

    def load(self):
        path = os.path.join(self.dir, 'logs.json')
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return []

    def save(self):
        path = os.path.join(self.dir, 'logs.json')
        with open(path, 'w') as f:
            json.dump(self.entries, f, indent=4)

    def log_time(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            spin_cycle = itertools.cycle(['-', '/', '|', '\''])

            def spin():
                while not self._stop:
                    elapsed = (time.perf_counter() - start) * 1000
                    print(f"\r{colored(next(spin_cycle) + ' Processing...', 'cyan', attrs=['bold'])} {elapsed:.2f} ms | CPU: {psutil.cpu_percent()}% | RAM: {psutil.virtual_memory().percent}%", end="")
                    time.sleep(0.1)

            self._stop = False
            spin_thread = threading.Thread(target=spin, daemon=True)
            spin_thread.start()

            result = func(*args, **kwargs)
            self._stop = True
            elapsed = (time.perf_counter() - start) * 1000
            print(f"\r{colored(f'✔️ {func.__name__} executed in {elapsed:.2f} ms.', 'green', attrs=['bold'])}")

            log_entry = {"timestamp": datetime.datetime.now().isoformat(), "level": "INFO", "message": f"Function '{func.__name__}' executed in {elapsed:.2f} ms."}
            self.entries.append(log_entry)
            self.save()
            self.log.info(f"Function '{func.__name__}' executed in {elapsed:.2f} ms.")
            self.times[func.__name__].append(elapsed)
            return result
        return wrapper

    def log(self, level, msg):
        self.errors[level] += 1
        entry = {"timestamp": datetime.datetime.now().isoformat(), "level": level.upper(), "message": msg}
        self.entries.append(entry)
        self.save()
        self.log.log(getattr(logging, level.upper(), logging.INFO), msg)

    def insights(self):
        env = {
            "Python": platform.python_version(), "OS": platform.system(), "OS Ver": platform.version(), "Machine": platform.machine(), "Processor": platform.processor(), "CPU Cores": psutil.cpu_count(), "Memory": f"{psutil.virtual_memory().total / (1024**3):.2f} GB", "Uptime (s)": (datetime.datetime.now() - self.start).total_seconds()
        }
        print(tabulate(env.items(), headers=["Metric", "Value"], tablefmt="fancy_grid"))
        
        if self.errors:
            plt.bar(*zip(*self.errors.items()), color='skyblue', edgecolor='black')
            plt.xlabel('Log Level')
            plt.ylabel('Count')
            plt.title('Log Level Distribution')
            plt.xticks(rotation=45)
            plt.savefig(os.path.join(self.dir, 'log_distribution.png'))
            plt.close()
            self.log.info("Log distribution graph saved.")

def main():
    try:
        log = InsightLog("InsightLog")

        @log.log_time
        def test_func():
            time.sleep(1.5)

        test_func()

        log.log("INFO", "This is an info log.")
        log.log("ERROR", "This is an error log.")
        log.log("SUCCESS", "This is a success log.")
        log.log("WARNING", "This is a warning log.")
        log.log("DEBUG", "This is a debug log.")
        log.log("CRITICAL", "This is a critical log.")

        log.insights()

    except Exception as e:
        print(colored(f"💥 Error: {e}", "red", attrs=["bold"]))

if __name__ == "__main__":
    main()