import logging
import datetime
import os
import time
import platform
import psutil
import threading
from termcolor import colored
import matplotlib.pyplot as plt
from collections import defaultdict
from logging.handlers import RotatingFileHandler
from tabulate import tabulate
import itertools
import sys
import io


def ensure_insight_folder():
    insight_dir = os.path.join(os.getcwd(), '.insight')  # Changed from '.Insight' to '.insight' to be consistent
    if not os.path.exists(insight_dir):
        os.makedirs(insight_dir)
    return insight_dir


def start_logging(name, save_log="enabled", log_dir=".insight", log_filename="app.log", max_bytes=1000000, backup_count=1, log_level=logging.DEBUG):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(log_level)

        if save_log == "enabled":
            if not os.path.isdir(log_dir):
                os.makedirs(log_dir)

            log_file = os.path.join(log_dir, log_filename)  # Using a single log file 'app.log'
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


class InsightLogger:
    def __init__(self, name, save_log="enabled", log_dir=".insight", log_filename="app.log", max_bytes=1000000, backup_count=1, log_level=logging.DEBUG):
        self.logger = start_logging(name, save_log, log_dir, log_filename, max_bytes, backup_count, log_level)
        self.insight_dir = ensure_insight_folder()
        self.error_count = defaultdict(int)
        self.start_time = datetime.datetime.now()

    def log_function_time(self, func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            spinner = itertools.cycle(['-', '\\', '|', '/'])
            elapsed_time_ms = 0

            def spin():
                nonlocal elapsed_time_ms
                while True:
                    elapsed_time_ms = (time.time() - start_time) * 1000
                    print(f"\r[{next(spinner)}] {elapsed_time_ms:.2f} ms", end="")
                    time.sleep(0.1)

            spin_thread = threading.Thread(target=spin, daemon=True)
            spin_thread.start()

            result = func(*args, **kwargs)

            elapsed_time_ms = (time.time() - start_time) * 1000
            print(f"\rFunction '{func.__name__}' executed in {elapsed_time_ms:.2f} ms.")
            self.logger.info(f"Function '{func.__name__}' executed in {elapsed_time_ms:.2f} ms.")
            return result
        return wrapper

    def format_message(self, level, text, bold=False, background=None, border=False, header=False, underline=False, urgent=False):
        color = {
            "INFO": "\033[92m",
            "SUCCESS": "\033[92m",
            "FAILURE": "\033[1;31m",
            "WARNING": "\033[93m",
            "DEBUG": "\033[94m",
            "ALERT": "\033[93m",
            "TRACE": "\033[96m",
            "HIGHLIGHT": "\033[1;33m",
            "BORDERED": "\033[1;34m",
            "HEADER": "\033[1;37m",
            "ERROR": "\033[91m",
            "CRITICAL": "\033[1;41m",
        }.get(level, "\033[0m")

        reset = "\033[0m"
        bold_style = "\033[1m" if bold else ""
        underline_style = "\033[4m" if underline else ""
        background_style = f"\033[48;5;226m" if background else ""
        urgent_style = "\033[5m" if urgent else ""

        return f"{color}{bold_style}{underline_style}{background_style}{urgent_style}{text}{reset}"

    def log_types(self, level, text):
        self.error_count[level] += 1
        if level == "INFO":
            self.logger.info(self.format_message("INFO", text))
        elif level == "ERROR":
            self.logger.error(self.format_message("ERROR", text))
        elif level == "SUCCESS":
            self.logger.info(self.format_message("SUCCESS", text))
        elif level == "FAILURE":
            self.logger.error(self.format_message("FAILURE", text))
        elif level == "WARNING":
            self.logger.warning(self.format_message("WARNING", text))
        elif level == "DEBUG":
            self.logger.debug(self.format_message("DEBUG", text))
        elif level == "ALERT":
            self.logger.warning(self.format_message("ALERT", text))
        elif level == "TRACE":
            self.logger.debug(self.format_message("TRACE", text))
        elif level == "HIGHLIGHT":
            self.logger.info(self.format_message("HIGHLIGHT", text))
        elif level == "CRITICAL":
            self.logger.critical(self.format_message("CRITICAL", text))

    def draw_and_save_graph(self):
        log_levels = list(self.error_count.keys())
        counts = list(self.error_count.values())

        fig, ax = plt.subplots()
        ax.bar(log_levels, counts, color='lightblue')
        ax.set_xlabel('Log Level')
        ax.set_ylabel('Frequency')
        ax.set_title('Log Level Frequency')
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()
        file_path = os.path.join(self.insight_dir, 'log_frequency.png')  # Save the graph in the '.insight' folder
        plt.savefig(file_path)
        plt.close()

        self.logger.info(f"Log frequency graph saved to {file_path}")

    def generate_log_summary(self):
        environment_info = {
            "Python Version": platform.python_version(),
            "Operating System": platform.system(),
            "OS Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "CPU Cores": psutil.cpu_count(),
            "Memory": f"{psutil.virtual_memory().total / (1024 * 1024 * 1024):.2f} GB",
            "Timestamp Started": self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "Timestamp Ended": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Run Duration (seconds)": (datetime.datetime.now() - self.start_time).total_seconds()
        }

        table_header = ["Environment Info", "Details"]
        table_rows = [(key, value) for key, value in environment_info.items()]
        table_footer = ["Total Errors", sum(self.error_count.values())]

        summary_table = tabulate(table_rows + [table_footer], headers=table_header, tablefmt="grid", numalign="right")

        return summary_table


def main():
    try:
        insight_logger = InsightLogger(name="InsightLog")

        @insight_logger.log_function_time
        def example_function():
            time.sleep(1.5)

        example_function()

        insight_logger.log_types("INFO", "This is an info log.")
        insight_logger.log_types("ERROR", "This is an error log.")
        insight_logger.log_types("SUCCESS", "This is a success log.")
        insight_logger.log_types("FAILURE", "This is a failure log.")
        insight_logger.log_types("WARNING", "This is a warning log.")
        insight_logger.log_types("DEBUG", "This is a debug log.")
        insight_logger.log_types("ALERT", "This is an alert log.")
        insight_logger.log_types("TRACE", "This is a trace log.")
        insight_logger.log_types("HIGHLIGHT", "This is a highlight log.")
        insight_logger.log_types("CRITICAL", "This is a critical log.")

        insight_logger.draw_and_save_graph()

        summary = insight_logger.generate_log_summary()
        insight_logger.logger.info("\nSummary of Logs:\n" + summary)

    except Exception as e:
        insight_logger.logger.error(f"Error initializing InsightLogger: {e}")


if __name__ == "__main__":
    main()
