import logging
import datetime
import os
import random
import time
import itertools
from tqdm import tqdm
from logging.handlers import RotatingFileHandler
from termcolor import colored


def start_logging(name, save_log="disabled", log_dir="./logs", log_filename=None, max_bytes=1000000, backup_count=1, log_level=logging.DEBUG):
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        logger.setLevel(log_level)

        if save_log == "enabled":
            if not os.path.isdir(log_dir):
                try:
                    os.mkdir(log_dir)
                    print(f"Log directory created at {log_dir}")
                except Exception as e:
                    print(f"Failed to create log directory: {e}")
                    raise

            if log_filename is None:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                log_filename = os.path.join(log_dir, f"{timestamp}-app.log")

            try:
                file_handler = RotatingFileHandler(log_filename, maxBytes=max_bytes, backupCount=backup_count)
                file_handler.setLevel(log_level)
                file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
                file_handler.setFormatter(file_formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                print(f"Failed to set up file handler: {e}")
                raise

        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        logger.debug(f"Logging initialized. Log file: {log_filename if save_log == 'enabled' else 'None'}")

    return logger


class CustomLogger:
    def __init__(self, name, save_log="disabled", log_dir="./logs", log_filename=None, max_bytes=1000000, backup_count=1, log_level=logging.DEBUG):
        self.logger = start_logging(name, save_log, log_dir, log_filename, max_bytes, backup_count, log_level)

    def info(self, text):
        self.logger.info(self.format_message("INFO", text))

    def warning(self, text):
        self.logger.warning(self.format_message("WARNING", text))

    def error(self, text):
        self.logger.error(self.format_message("ERROR", text))

    def debug(self, text):
        self.logger.debug(self.format_message("DEBUG", text))

    def critical(self, text):
        self.logger.critical(self.format_message("CRITICAL", text))

    def success(self, text):
        self.logger.info(self.format_message("SUCCESS", text))

    def failure(self, text):
        self.logger.error(self.format_message("FAILURE", text))

    def alert(self, text):
        self.logger.warning(self.format_message("ALERT", text))

    def trace(self, text):
        self.logger.debug(self.format_message("TRACE", text))

    def highlight(self, text):
        self.logger.info(self.format_message("HIGHLIGHT", text, background="yellow", bold=True))

    def bordered(self, text):
        self.logger.info(self.format_message("BORDERED", text, border=True))

    def header(self, text):
        self.logger.info(self.format_message("HEADER", text, header=True))

    def debug_underline(self, text):
        self.logger.debug(self.format_message("DEBUG UNDERLINE", text, underline=True))

    def alert_urgent(self, text):
        self.logger.error(self.format_message("ALERT URGENT", text, urgent=True))

    def format_message(self, level, text, bold=False, background=None, border=False, header=False, underline=False, urgent=False):
        color = {
            "INFO": "\033[92m",  
            "WARNING": "\033[93m",  
            "ERROR": "\033[91m",  
            "DEBUG": "\033[94m",  
            "CRITICAL": "\033[1;41m",  
            "SUCCESS": "\033[92m",  
            "FAILURE": "\033[1;31m",  
            "ALERT": "\033[93m",  
            "TRACE": "\033[96m",  
            "HIGHLIGHT": "\033[1;33m",  
            "BORDERED": "\033[1;34m",  
            "HEADER": "\033[1;37m",  
            "DEBUG UNDERLINE": "\033[4m",  
            "ALERT URGENT": "\033[5;1;31m",
        }.get(level, "\033[0m")  

        reset = "\033[0m"
        bold_style = "\033[1m" if bold else ""
        underline_style = "\033[4m" if underline else ""
        background_style = f"\033[48;5;226m" if background else ""
        urgent_style = "\033[5m" if urgent else ""

        border_style = "\033[1;37m" if border else ""

        if border:
            return f"{border_style}+{'-' * (len(text) + 2)}+\n| {text} |\n+{'-' * (len(text) + 2)}+"

        if header:
            return f"{bold_style}{color}{text}{reset}"

        return f"{color}{bold_style}{underline_style}{background_style}{urgent_style}{text}{reset}"

    def draw_progress_bar(self, total=100, duration=5, description="Lädt...", color='green'):
        step_duration = duration / total
        pbar = tqdm(total=total, desc=description, ncols=100, ascii=True, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed} < {remaining}]")
        pbar.set_postfix(color=color)
        for i in range(total):
            time.sleep(step_duration)
            pbar.update(1)
        pbar.close()

    def draw_bar_chart(self, values=None):
        if values is None:
            values = {"A": random.randint(1, 10), "B": random.randint(1, 10), "C": random.randint(1, 10)}

        print("\nSäulendiagramm (ASCII):")
        max_height = max(values.values())
        for i in range(max_height, 0, -1):
            for key in values:
                if values[key] >= i:
                    print("█", end="  ")
                else:
                    print("   ", end="  ")
            print()
        print("   " + "  ".join(values.keys()))

    def draw_pie_chart(self, values=None):
        if values is None:
            values = {"A": 30, "B": 50, "C": 20}

        print("\nKreisdiagramm (ASCII):")
        total = sum(values.values())
        for key, value in values.items():
            percentage = (value / total) * 100
            print(f"{key}: {'#' * int(percentage // 2)} ({percentage:.2f}%)")

    def draw_line_chart(self, values=None):
        if values is None:
            values = [random.randint(1, 10) for _ in range(10)]
        
        print("\nLiniendiagramm (ASCII):")
        for i, value in enumerate(values):
            print(f"{i+1}: {'-'*value} ({value})")

    def draw_scatter_plot(self, values=None):
        if values is None:
            values = [(random.randint(1, 10), random.randint(1, 10)) for _ in range(10)]
        
        print("\nPunkt-Diagramm (ASCII):")
        for x, y in values:
            print(f"({x},{y})", end=" ")
        print()

    def draw_waterfall_chart(self, values=None):
        if values is None:
            values = [5, -3, 8, -2, 4]

        print("\nWasserfall-Diagramm:")
        current = 0
        for value in values:
            current += value
            print(f" {current:4d} {'▲' if value > 0 else '▼'} {value:3d}")

    def draw_circular_progress(self, current, total):
        progress = (current / total) * 100
        progress_bar = "◉" * int(progress // 10) + "○" * (10 - int(progress // 10))
        print(f"Kreisförmiger Fortschritt: {progress:.2f}% [{progress_bar}]")

    def display_percentage(self, current, total):
        percent = (current / total) * 100
        print(f"{'='*int(percent//2)} {percent:.2f}%")

    def print_table(self, data, headers=None):
        print("\nTabellen-Darstellung:")
        if headers:
            print(f"{' | '.join(headers)}")
        for row in data:
            print(f"{' | '.join(str(cell) for cell in row)}")

    def print_ascii_art(self, text):
        print(f"\nASCII-Art Darstellung: \n{text}")

    def color_gradient(self, text, start_color="red", end_color="yellow"):
        gradient = self.create_gradient(text, start_color, end_color)
        print(f"\nFarb-Gradient: \n{gradient}")

    def create_gradient(self, text, start_color, end_color):
        colors = ['red', 'yellow', 'green', 'blue', 'cyan', 'magenta', 'white']
        start_index = colors.index(start_color)
        end_index = colors.index(end_color)
        gradient_text = ""
        step = (end_index - start_index) // len(text)
        for i, char in enumerate(text):
            color = colors[(start_index + step * i) % len(colors)]
            gradient_text += colored(char, color)
        return gradient_text

    def spin_animation(self, duration=5):
        spinner = itertools.cycle(['|', '/', '-', '\\'])
        end_time = time.time() + duration
        while time.time() < end_time:
            print(f"\r{next(spinner)}", end="")
            time.sleep(0.1)


if __name__ == "__main__":
    try:
        log_instance = CustomLogger(name="Hii")
        
        log_instance.success("This is a success log.")
        log_instance.failure("This is a failure log.")
        log_instance.alert("This is an alert log.")
        log_instance.trace("This is a trace log.")
        log_instance.highlight("This is a highlighted log.")
        log_instance.bordered("This is a bordered log.")
        log_instance.header("This is a header log.")
        log_instance.debug_underline("This is a debug underline log.")
        log_instance.alert_urgent("This is an urgent alert log.")

        log_instance.draw_bar_chart()
        log_instance.draw_pie_chart()
        log_instance.draw_line_chart()
        log_instance.draw_scatter_plot()
        log_instance.draw_waterfall_chart()

        log_instance.draw_progress_bar(total=100, duration=5, description="Loading...")
        
        data = [["Name", "Age", "Location"], ["John", 30, "New York"], ["Jane", 25, "Los Angeles"]]
        log_instance.print_table(data)
        log_instance.print_ascii_art("Sample ASCII Art")
        log_instance.color_gradient("Gradient Text", start_color="red", end_color="blue")
        log_instance.spin_animation(duration=5)

    except Exception as e:
        logging.error(f"Fehler bei der Initialisierung des Loggers: {e}")
