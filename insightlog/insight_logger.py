import logging
import datetime
import os
import time
import platform
import psutil
import threading
import itertools
import json
import hashlib
import smtplib
import subprocess
import traceback
import warnings
import sqlite3
import pickle
import gzip
import signal
import urllib.request
import ssl
from collections import defaultdict, deque
from logging.handlers import RotatingFileHandler, SMTPHandler, TimedRotatingFileHandler
from termcolor import colored
from tabulate import tabulate
from functools import wraps
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from contextlib import contextmanager
from pathlib import Path
import sys
import io

# Optional matplotlib import with graceful fallback
try:
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    plt = None
    np = None
    MATPLOTLIB_AVAILABLE = False
    warnings.warn("matplotlib and/or numpy not available. Visualization features will be disabled. "
                 "Install with: pip install matplotlib numpy", ImportWarning)

# Set the default encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Version information
__version__ = "1.4.0"
__author__ = "Velyzo"
__license__ = "MIT"

# Helper functions for safe numpy operations
def safe_mean(values):
    """Calculate mean with fallback when numpy is not available"""
    if not values:
        return 0
    if MATPLOTLIB_AVAILABLE and np is not None:
        return np.mean(values)
    return sum(values) / len(values)

def safe_std(values):
    """Calculate standard deviation with fallback when numpy is not available"""
    if not values:
        return 0
    if MATPLOTLIB_AVAILABLE and np is not None:
        return np.std(values)
    # Simple standard deviation calculation
    mean_val = safe_mean(values)
    variance = sum((x - mean_val) ** 2 for x in values) / len(values)
    return variance ** 0.5

def safe_polyfit(x, y, degree=1):
    """Linear regression with fallback when numpy is not available"""
    if MATPLOTLIB_AVAILABLE and np is not None:
        return np.polyfit(x, y, degree)
    # Simple linear regression for degree=1
    if len(x) != len(y) or len(x) < 2:
        return [0, 0]
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(x[i] * y[i] for i in range(n))
    sum_x2 = sum(x[i] ** 2 for i in range(n))
    
    # Calculate slope and intercept
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    intercept = (sum_y - slope * sum_x) / n
    return [slope, intercept]

# Ensure Insight Folder Creation
def ensure_insight_folder():
    insight_dir = os.path.join(os.getcwd(), '.insight')
    if not os.path.exists(insight_dir):
        os.makedirs(insight_dir)
    return insight_dir

# Logger Initialization with Rotating File Handler
def start_logging(name, save_log="enabled", log_dir=".insight", log_filename="app.log", max_bytes=1000000, backup_count=1, log_level=logging.DEBUG):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(log_level)

        if save_log == "enabled":
            if not os.path.isdir(log_dir):
                os.makedirs(log_dir)

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

# Enhanced InsightLogger Class with Advanced Features v1.4
class InsightLogger:
    """
    Advanced logging utility with comprehensive monitoring, analytics, and reporting capabilities.
    
    Features in v1.4:
    - Real-time monitoring dashboard
    - Performance profiling
    - Memory usage tracking
    - Network monitoring
    - Database logging
    - Email alerts
    - Log aggregation and analysis
    - Security monitoring
    - Plugin system
    - API monitoring
    - Custom metrics
    - Export capabilities
    """
    
    def __init__(self, name, save_log="enabled", log_dir=".insight", log_filename="app.log", 
                 max_bytes=1000000, backup_count=1, log_level=logging.DEBUG, 
                 enable_database=True, enable_monitoring=True, enable_alerts=False,
                 alert_email=None, smtp_server=None, smtp_port=587, smtp_user=None, smtp_password=None):
        
        self.logger = start_logging(name, save_log, log_dir, log_filename, max_bytes, backup_count, log_level)
        self.insight_dir = ensure_insight_folder()
        self.name = name
        
        # Core tracking dictionaries
        self.error_count = defaultdict(int)
        self.execution_times = defaultdict(list)
        self.function_error_count = defaultdict(int)
        self.memory_usage = deque(maxlen=1000)
        self.cpu_usage = deque(maxlen=1000)
        self.network_stats = defaultdict(list)
        self.custom_metrics = defaultdict(list)
        self.security_events = []
        self.api_calls = defaultdict(list)
        
        # Performance profiling
        self.profiling_data = defaultdict(dict)
        self.call_stack = []
        self.bottlenecks = []
        
        # Configuration
        self.start_time = datetime.datetime.now()
        self.session_id = hashlib.md5(f"{name}{self.start_time}".encode()).hexdigest()[:8]
        self.enable_monitoring = enable_monitoring
        self.enable_alerts = enable_alerts
        self.alert_thresholds = {
            'cpu_usage': 80,
            'memory_usage': 85,
            'error_rate': 10,
            'response_time': 5000
        }
        
        # Email configuration
        self.alert_email = alert_email
        self.smtp_config = {
            'server': smtp_server,
            'port': smtp_port,
            'user': smtp_user,
            'password': smtp_password
        } if all([smtp_server, smtp_user, smtp_password]) else None
        
        # Database setup
        if enable_database:
            self._setup_database()
        
        # Monitoring thread
        if enable_monitoring:
            self._start_monitoring()
        
        # Plugin system
        self.plugins = {}
        self._load_plugins()

    def _setup_database(self):
        """Setup SQLite database for persistent logging"""
        self.db_path = os.path.join(self.insight_dir, f"insights_{self.session_id}.db")
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                level TEXT,
                message TEXT,
                function_name TEXT,
                execution_time REAL,
                memory_usage REAL,
                cpu_usage REAL,
                session_id TEXT
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                metric_name TEXT,
                metric_value REAL,
                session_id TEXT
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS security_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                event_type TEXT,
                severity TEXT,
                description TEXT,
                session_id TEXT
            )
        ''')
        self.conn.commit()

    def _start_monitoring(self):
        """Start background monitoring thread"""
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_system, daemon=True)
        self.monitor_thread.start()

    def _monitor_system(self):
        """Background system monitoring"""
        while self.monitoring_active:
            try:
                # CPU and Memory monitoring
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                
                self.cpu_usage.append({
                    'timestamp': datetime.datetime.now(),
                    'value': cpu_percent
                })
                
                self.memory_usage.append({
                    'timestamp': datetime.datetime.now(),
                    'value': memory.percent
                })
                
                # Check thresholds and send alerts
                if self.enable_alerts:
                    self._check_alert_thresholds(cpu_percent, memory.percent)
                
                # Network monitoring
                net_io = psutil.net_io_counters()
                self.network_stats['bytes_sent'].append(net_io.bytes_sent)
                self.network_stats['bytes_recv'].append(net_io.bytes_recv)
                
                time.sleep(5)  # Monitor every 5 seconds
                
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")

    def _check_alert_thresholds(self, cpu_percent, memory_percent):
        """Check if system metrics exceed thresholds and send alerts"""
        alerts = []
        
        if cpu_percent > self.alert_thresholds['cpu_usage']:
            alerts.append(f"High CPU usage: {cpu_percent:.1f}%")
        
        if memory_percent > self.alert_thresholds['memory_usage']:
            alerts.append(f"High memory usage: {memory_percent:.1f}%")
        
        if alerts and self.smtp_config and self.alert_email:
            self._send_alert_email(alerts)

    def _send_alert_email(self, alerts):
        """Send alert emails for critical events"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config['user']
            msg['To'] = self.alert_email
            msg['Subject'] = f"InsightLog Alert - {self.name}"
            
            body = f"""
            Alert from InsightLogger ({self.name})
            Session ID: {self.session_id}
            Time: {datetime.datetime.now()}
            
            Alerts:
            {chr(10).join([f"- {alert}" for alert in alerts])}
            
            System Information:
            - CPU Usage: {self.cpu_usage[-1]['value'] if self.cpu_usage else 'N/A'}%
            - Memory Usage: {self.memory_usage[-1]['value'] if self.memory_usage else 'N/A'}%
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port'])
            server.starttls()
            server.login(self.smtp_config['user'], self.smtp_config['password'])
            server.send_message(msg)
            server.quit()
            
            self.logger.info("Alert email sent successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to send alert email: {e}")

    def _load_plugins(self):
        """Load available plugins"""
        plugin_dir = os.path.join(self.insight_dir, 'plugins')
        if os.path.exists(plugin_dir):
            for file in os.listdir(plugin_dir):
                if file.endswith('.py') and not file.startswith('__'):
                    try:
                        plugin_name = file[:-3]
                        # Dynamic plugin loading would go here
                        self.logger.info(f"Plugin {plugin_name} loaded")
                    except Exception as e:
                        self.logger.error(f"Failed to load plugin {file}: {e}")

    @contextmanager
    def performance_profile(self, operation_name):
        """Context manager for performance profiling"""
        start_time = time.perf_counter()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        try:
            yield
        finally:
            end_time = time.perf_counter()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            execution_time = (end_time - start_time) * 1000  # ms
            memory_delta = end_memory - start_memory
            
            self.profiling_data[operation_name] = {
                'execution_time': execution_time,
                'memory_delta': memory_delta,
                'timestamp': datetime.datetime.now()
            }
            
            self.logger.info(f"Profile {operation_name}: {execution_time:.2f}ms, Memory: {memory_delta:+.2f}MB")

    def track_api_call(self, endpoint, method="GET", response_time=None, status_code=None):
        """Track API call metrics"""
        call_data = {
            'timestamp': datetime.datetime.now(),
            'endpoint': endpoint,
            'method': method,
            'response_time': response_time,
            'status_code': status_code
        }
        
        self.api_calls[endpoint].append(call_data)
        
        if hasattr(self, 'conn'):
            self.conn.execute('''
                INSERT INTO metrics (timestamp, metric_name, metric_value, session_id)
                VALUES (?, ?, ?, ?)
            ''', (call_data['timestamp'].isoformat(), f"api_response_time_{endpoint}", 
                  response_time or 0, self.session_id))
            self.conn.commit()

    def add_custom_metric(self, metric_name, value, tags=None):
        """Add custom application metrics"""
        metric_data = {
            'timestamp': datetime.datetime.now(),
            'value': value,
            'tags': tags or {}
        }
        
        self.custom_metrics[metric_name].append(metric_data)
        
        if hasattr(self, 'conn'):
            self.conn.execute('''
                INSERT INTO metrics (timestamp, metric_name, metric_value, session_id)
                VALUES (?, ?, ?, ?)
            ''', (metric_data['timestamp'].isoformat(), metric_name, value, self.session_id))
            self.conn.commit()

    def log_security_event(self, event_type, severity="MEDIUM", description=""):
        """Log security-related events"""
        security_event = {
            'timestamp': datetime.datetime.now(),
            'event_type': event_type,
            'severity': severity,
            'description': description
        }
        
        self.security_events.append(security_event)
        
        if hasattr(self, 'conn'):
            self.conn.execute('''
                INSERT INTO security_events (timestamp, event_type, severity, description, session_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (security_event['timestamp'].isoformat(), event_type, severity, 
                  description, self.session_id))
            self.conn.commit()
        
        color = 'red' if severity == 'HIGH' else 'yellow' if severity == 'MEDIUM' else 'cyan'
        self.logger.warning(colored(f"🔒 SECURITY: {event_type} - {description}", color, attrs=['bold']))

    def detect_anomalies(self):
        """Detect anomalies in system metrics and performance"""
        if not MATPLOTLIB_AVAILABLE:
            self.logger.debug("NumPy not available for anomaly detection")
            return []
            
        anomalies = []
        
        # CPU usage anomalies
        if len(self.cpu_usage) > 10:
            recent_cpu = [item['value'] for item in list(self.cpu_usage)[-10:]]
            if safe_std(recent_cpu) > 20:  # High variance
                anomalies.append("High CPU usage variance detected")
        
        # Memory usage trend
        if len(self.memory_usage) > 20:
            recent_memory = [item['value'] for item in list(self.memory_usage)[-20:]]
            if safe_polyfit(range(len(recent_memory)), recent_memory, 1)[0] > 1:  # Increasing trend
                anomalies.append("Memory usage increasing trend detected")
        
        # Error rate anomaly
        total_logs = sum(self.error_count.values())
        error_logs = self.error_count.get('ERROR', 0) + self.error_count.get('CRITICAL', 0)
        if total_logs > 0 and (error_logs / total_logs) > 0.2:  # >20% error rate
            anomalies.append(f"High error rate detected: {(error_logs/total_logs)*100:.1f}%")
        
        return anomalies

    def generate_performance_report(self):
        """Generate comprehensive performance report"""
        report = {
            'session_info': {
                'session_id': self.session_id,
                'start_time': self.start_time.isoformat(),
                'duration': str(datetime.datetime.now() - self.start_time),
                'total_logs': sum(self.error_count.values())
            },
            'system_metrics': {},
            'function_performance': {},
            'anomalies': self.detect_anomalies(),
            'security_events': len(self.security_events)
        }
        
        # System metrics with fallback for missing numpy
        if self.cpu_usage and self.memory_usage:
            report['system_metrics'] = {
                'avg_cpu_usage': safe_mean([item['value'] for item in self.cpu_usage]),
                'max_cpu_usage': max([item['value'] for item in self.cpu_usage]),
                'avg_memory_usage': safe_mean([item['value'] for item in self.memory_usage]),
                'max_memory_usage': max([item['value'] for item in self.memory_usage])
            }
        
        # Function performance summary
        for func_name, times in self.execution_times.items():
            report['function_performance'][func_name] = {
                'call_count': len(times),
                'avg_time': safe_mean(times),
                'min_time': min(times),
                'max_time': max(times),
                'total_time': sum(times)
            }
        
        return report

    def export_data(self, format_type="json", include_raw_data=False):
        """Export logging data in various formats"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type.lower() == "json":
            export_data = {
                'metadata': {
                    'export_time': datetime.datetime.now().isoformat(),
                    'session_id': self.session_id,
                    'logger_name': self.name,
                    'version': __version__
                },
                'performance_report': self.generate_performance_report(),
                'log_summary': self.error_count,
                'custom_metrics': {k: len(v) for k, v in self.custom_metrics.items()}
            }
            
            if include_raw_data:
                export_data['raw_data'] = {
                    'cpu_usage': list(self.cpu_usage),
                    'memory_usage': list(self.memory_usage),
                    'execution_times': dict(self.execution_times),
                    'security_events': self.security_events
                }
            
            filename = f"insight_export_{timestamp}.json"
            filepath = os.path.join(self.insight_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
                
        elif format_type.lower() == "csv":
            import csv
            filename = f"insight_export_{timestamp}.csv"
            filepath = os.path.join(self.insight_dir, filename)
            
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Metric', 'Value'])
                
                for level, count in self.error_count.items():
                    writer.writerow([f'Log_{level}', count])
                
                for func, times in self.execution_times.items():
                    writer.writerow([f'Func_{func}_avg_time', safe_mean(times)])
                    writer.writerow([f'Func_{func}_call_count', len(times)])
        
        self.logger.info(f"Data exported to {filepath}")
        return filepath

    def create_dashboard_html(self):
        """Create an HTML dashboard for real-time monitoring"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>InsightLog Dashboard - {self.name}</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; margin: -20px -20px 20px -20px; }}
                .metric-card {{ background: white; padding: 15px; margin: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); display: inline-block; min-width: 200px; }}
                .chart-container {{ background: white; padding: 20px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                .status-green {{ color: #27ae60; }}
                .status-red {{ color: #e74c3c; }}
                .status-yellow {{ color: #f39c12; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔍 InsightLog Dashboard</h1>
                <p>Logger: {self.name} | Session: {self.session_id} | Version: {__version__}</p>
            </div>
            
            <div class="metric-card">
                <h3>System Status</h3>
                <p>CPU: <span class="status-{'green' if self.cpu_usage and self.cpu_usage[-1]['value'] < 70 else 'yellow' if self.cpu_usage and self.cpu_usage[-1]['value'] < 90 else 'red'}">{self.cpu_usage[-1]['value']:.1f}%</span></p>
                <p>Memory: <span class="status-{'green' if self.memory_usage and self.memory_usage[-1]['value'] < 70 else 'yellow' if self.memory_usage and self.memory_usage[-1]['value'] < 90 else 'red'}">{self.memory_usage[-1]['value']:.1f}%</span></p>
            </div>
            
            <div class="metric-card">
                <h3>Logging Statistics</h3>
                <p>Total Logs: {sum(self.error_count.values())}</p>
                <p>Errors: {self.error_count.get('ERROR', 0)}</p>
                <p>Security Events: {len(self.security_events)}</p>
            </div>
            
            <div class="metric-card">
                <h3>Performance</h3>
                <p>Functions Tracked: {len(self.execution_times)}</p>
                <p>Custom Metrics: {len(self.custom_metrics)}</p>
                <p>Uptime: {datetime.datetime.now() - self.start_time}</p>
            </div>
            
            <div class="chart-container">
                <h3>System Resource Usage</h3>
                <div id="systemChart"></div>
            </div>
            
            <script>
                // JavaScript for live updating charts would go here
                // This is a simplified static version
                var trace1 = {{
                    x: {[f"'{item['timestamp'].strftime('%H:%M:%S')}'" for item in list(self.cpu_usage)[-20:]]},
                    y: {[item['value'] for item in list(self.cpu_usage)[-20:]]},
                    type: 'scatter',
                    name: 'CPU Usage %'
                }};
                
                var trace2 = {{
                    x: {[f"'{item['timestamp'].strftime('%H:%M:%S')}'" for item in list(self.memory_usage)[-20:]]},
                    y: {[item['value'] for item in list(self.memory_usage)[-20:]]},
                    type: 'scatter',
                    name: 'Memory Usage %'
                }};
                
                Plotly.newPlot('systemChart', [trace1, trace2]);
            </script>
        </body>
        </html>
        """
        
        dashboard_path = os.path.join(self.insight_dir, f"dashboard_{self.session_id}.html")
        with open(dashboard_path, 'w') as f:
            f.write(html_content)
        
        self.logger.info(f"Dashboard created: {dashboard_path}")
        return dashboard_path

    def log_function_time(self, func):
        """Enhanced function timing decorator with profiling"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            # Enhanced spinner with more information
            spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
            elapsed_time_ms = 0
            
            def spin():
                nonlocal elapsed_time_ms
                while not self._stop_spin:
                    elapsed_time_ms = (time.perf_counter() - start_time) * 1000
                    memory_now = psutil.Process().memory_info().rss / 1024 / 1024
                    print(f"\r{colored(f'{next(spinner)} {func.__name__}()', 'cyan', attrs=['bold'])} "
                          f"{elapsed_time_ms:.1f}ms | {memory_now:.1f}MB", end="", flush=True)
                    time.sleep(0.1)
            
            self._stop_spin = False
            spin_thread = threading.Thread(target=spin, daemon=True)
            spin_thread.start()
            
            try:
                result = func(*args, **kwargs)
                success = True
                error_msg = None
            except Exception as e:
                success = False
                error_msg = str(e)
                self.function_error_count[func.__name__] += 1
                raise
            finally:
                self._stop_spin = True
                spin_thread.join(timeout=0.1)
                
                end_time = time.perf_counter()
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024
                elapsed_time_ms = (end_time - start_time) * 1000
                memory_delta = end_memory - start_memory
                
                # Enhanced logging with more metrics
                status_icon = "✅" if success else "❌"
                status_color = "green" if success else "red"
                
                print(f"\r{colored(f'{status_icon} {func.__name__}()', status_color, attrs=['bold'])} "
                      f"{elapsed_time_ms:.2f}ms | Δ{memory_delta:+.1f}MB")
                
                log_msg = f"Function '{func.__name__}' executed in {elapsed_time_ms:.2f}ms (Memory: {memory_delta:+.1f}MB)"
                if not success:
                    log_msg += f" - ERROR: {error_msg}"
                
                self.logger.info(log_msg)
                self.execution_times[func.__name__].append(elapsed_time_ms)
                
                # Store in database if available
                if hasattr(self, 'conn'):
                    self.conn.execute('''
                        INSERT INTO logs (timestamp, level, message, function_name, execution_time, memory_usage, session_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (datetime.datetime.now().isoformat(), 'INFO' if success else 'ERROR', 
                          log_msg, func.__name__, elapsed_time_ms, memory_delta, self.session_id))
                    self.conn.commit()
            
            return result
        return wrapper

    def format_message(self, level, text, bold=False, background=None, border=False, header=False, underline=False, urgent=False, emoji=True):
        """Enhanced message formatting with emoji support"""
        colors = {
            "INFO": "cyan",
            "SUCCESS": "green", 
            "FAILURE": "red",
            "WARNING": "yellow",
            "DEBUG": "blue",
            "ALERT": "magenta",
            "TRACE": "cyan",
            "HIGHLIGHT": "yellow",
            "BORDERED": "blue",
            "HEADER": "white",
            "ERROR": "red",
            "CRITICAL": "red",
        }
        
        emojis = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "FAILURE": "❌", 
            "WARNING": "⚠️",
            "DEBUG": "🐛",
            "ALERT": "🚨",
            "TRACE": "🔍",
            "HIGHLIGHT": "⭐",
            "ERROR": "💥",
            "CRITICAL": "🔥",
        } if emoji else {}
        
        color = colors.get(level, "white")
        emoji_prefix = f"{emojis.get(level, '')} " if emoji and level in emojis else ""
        
        attrs = []
        if bold: attrs.append('bold')
        if underline: attrs.append('underline')
        if urgent: attrs.append('blink')
        
        formatted_text = f"{emoji_prefix}{text}"
        
        if border:
            border_char = "=" if header else "-"
            border_line = border_char * (len(text) + 10)
            formatted_text = f"\n{border_line}\n{formatted_text}\n{border_line}"
        
        return colored(formatted_text, color, attrs=attrs if attrs else None)

    def log_types(self, level, text, **kwargs):
        """Enhanced logging with additional context and database storage"""
        self.error_count[level] += 1
        formatted_msg = self.format_message(level, text, **kwargs)
        
        # Current system state
        cpu_usage = psutil.cpu_percent() if hasattr(psutil, 'cpu_percent') else 0
        memory_usage = psutil.virtual_memory().percent if hasattr(psutil, 'virtual_memory') else 0
        
        # Log to appropriate level
        log_methods = {
            "INFO": self.logger.info,
            "ERROR": self.logger.error,
            "SUCCESS": self.logger.info,
            "FAILURE": self.logger.error,
            "WARNING": self.logger.warning,
            "DEBUG": self.logger.debug,
            "ALERT": self.logger.warning,
            "TRACE": self.logger.debug,
            "HIGHLIGHT": self.logger.info,
            "CRITICAL": self.logger.critical,
        }
        
        log_method = log_methods.get(level, self.logger.info)
        log_method(formatted_msg)
        
        # Store in database if available
        if hasattr(self, 'conn'):
            self.conn.execute('''
                INSERT INTO logs (timestamp, level, message, cpu_usage, memory_usage, session_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (datetime.datetime.now().isoformat(), level, text, cpu_usage, memory_usage, self.session_id))
            self.conn.commit()
        
        # Check for alert conditions
        if level in ['ERROR', 'CRITICAL'] and self.enable_alerts:
            self._check_error_rate_alert()

    def _check_error_rate_alert(self):
        """Check if error rate exceeds threshold"""
        total_logs = sum(self.error_count.values())
        error_logs = self.error_count.get('ERROR', 0) + self.error_count.get('CRITICAL', 0)
        
        if total_logs > 10:  # Only check after minimum logs
            error_rate = (error_logs / total_logs) * 100
            if error_rate > self.alert_thresholds['error_rate']:
                if self.smtp_config and self.alert_email:
                    self._send_alert_email([f"High error rate: {error_rate:.1f}%"])

    def batch_log(self, logs):
        """Process multiple logs efficiently"""
        for log_entry in logs:
            if isinstance(log_entry, dict):
                level = log_entry.get('level', 'INFO')
                message = log_entry.get('message', '')
                kwargs = {k: v for k, v in log_entry.items() if k not in ['level', 'message']}
                self.log_types(level, message, **kwargs)
            elif isinstance(log_entry, tuple) and len(log_entry) >= 2:
                level, message = log_entry[:2]
                self.log_types(level, message)
        
        self.logger.info(f"Processed {len(logs)} log entries in batch")

    def log_with_context(self, level, message, context=None, tags=None):
        """Log with additional context information"""
        context = context or {}
        tags = tags or []
        
        # Add system context
        context.update({
            'timestamp': datetime.datetime.now().isoformat(),
            'session_id': self.session_id,
            'function': context.get('function', 'unknown'),
            'line_number': context.get('line_number', 'unknown'),
            'cpu_usage': psutil.cpu_percent(),
            'memory_usage': psutil.virtual_memory().percent
        })
        
        # Format message with context
        if context or tags:
            context_str = f" | Context: {json.dumps(context, default=str)}" if context else ""
            tags_str = f" | Tags: {', '.join(tags)}" if tags else ""
            full_message = f"{message}{context_str}{tags_str}"
        else:
            full_message = message
        
        self.log_types(level, full_message)

    def create_log_filter(self, level=None, start_time=None, end_time=None, function_name=None):
        """Create filtered view of logs"""
        if not hasattr(self, 'conn'):
            return []
        
        query = "SELECT * FROM logs WHERE 1=1"
        params = []
        
        if level:
            query += " AND level = ?"
            params.append(level)
        
        if start_time:
            query += " AND timestamp >= ?"
            params.append(start_time.isoformat())
        
        if end_time:
            query += " AND timestamp <= ?"
            params.append(end_time.isoformat())
        
        if function_name:
            query += " AND function_name = ?"
            params.append(function_name)
        
        query += " ORDER BY timestamp DESC"
        
        cursor = self.conn.execute(query, params)
        return cursor.fetchall()

    def get_function_statistics(self):
        """Get detailed statistics for all tracked functions"""
        stats = {}
        
        for func_name, times in self.execution_times.items():
            if times:
                stats[func_name] = {
                    'call_count': len(times),
                    'avg_time': safe_mean(times),
                    'min_time': min(times),
                    'max_time': max(times),
                    'total_time': sum(times),
                    'std_dev': safe_std(times),
                    'error_count': self.function_error_count.get(func_name, 0),
                    'success_rate': ((len(times) - self.function_error_count.get(func_name, 0)) / len(times)) * 100
                }
        
        return stats

    def compress_logs(self, older_than_days=7):
        """Compress old log files to save space"""
        log_dir = Path(self.insight_dir)
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=older_than_days)
        
        compressed_count = 0
        for log_file in log_dir.glob("*.log"):
            if log_file.stat().st_mtime < cutoff_date.timestamp():
                compressed_file = log_file.with_suffix('.log.gz')
                
                with open(log_file, 'rb') as f_in:
                    with gzip.open(compressed_file, 'wb') as f_out:
                        f_out.writelines(f_in)
                
                log_file.unlink()  # Remove original
                compressed_count += 1
        
        self.logger.info(f"Compressed {compressed_count} old log files")
        return compressed_count

    def draw_and_save_graph(self, graph_type="all"):
        """Enhanced graph generation with multiple chart types"""
        if not MATPLOTLIB_AVAILABLE:
            self.logger.warning("Matplotlib not available. Skipping graph generation. Install with: pip install matplotlib numpy")
            return
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if graph_type in ["all", "log_frequency"]:
            # Log Level Frequency Bar Chart
            if self.error_count:
                log_levels = list(self.error_count.keys())
                counts = list(self.error_count.values())
                
                fig, ax = plt.subplots(figsize=(12, 6))
                bars = ax.bar(log_levels, counts, color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6'])
                
                # Add value labels on bars
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{int(height)}', ha='center', va='bottom', fontweight='bold')
                
                ax.set_xlabel('Log Level', fontsize=12, fontweight='bold')
                ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
                ax.set_title(f'Log Level Frequency - {self.name}', fontsize=14, fontweight='bold')
                ax.tick_params(axis='x', rotation=45)
                plt.tight_layout()
                
                file_path = os.path.join(self.insight_dir, f'log_frequency_{timestamp}.png')
                plt.savefig(file_path, dpi=300, bbox_inches='tight')
                plt.close()
                
                self.logger.info(f"Log frequency graph saved to {file_path}")
        
        if graph_type in ["all", "system_metrics"] and (self.cpu_usage or self.memory_usage):
            # System Metrics Time Series
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
            
            if self.cpu_usage:
                cpu_times = [item['timestamp'] for item in self.cpu_usage]
                cpu_values = [item['value'] for item in self.cpu_usage]
                ax1.plot(cpu_times, cpu_values, 'b-', linewidth=2, label='CPU Usage %')
                ax1.fill_between(cpu_times, cpu_values, alpha=0.3)
                ax1.set_ylabel('CPU Usage (%)', fontweight='bold')
                ax1.set_title('System CPU Usage Over Time', fontweight='bold')
                ax1.grid(True, alpha=0.3)
                ax1.legend()
            
            if self.memory_usage:
                mem_times = [item['timestamp'] for item in self.memory_usage]
                mem_values = [item['value'] for item in self.memory_usage]
                ax2.plot(mem_times, mem_values, 'r-', linewidth=2, label='Memory Usage %')
                ax2.fill_between(mem_times, mem_values, alpha=0.3, color='red')
                ax2.set_ylabel('Memory Usage (%)', fontweight='bold')
                ax2.set_xlabel('Time', fontweight='bold')
                ax2.set_title('System Memory Usage Over Time', fontweight='bold')
                ax2.grid(True, alpha=0.3)
                ax2.legend()
            
            plt.tight_layout()
            file_path = os.path.join(self.insight_dir, f'system_metrics_{timestamp}.png')
            plt.savefig(file_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"System metrics graph saved to {file_path}")
        
        if graph_type in ["all", "function_performance"] and self.execution_times:
            # Function Performance Analysis
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
            
            # Average execution times
            func_names = list(self.execution_times.keys())
            avg_times = [safe_mean(self.execution_times[func]) for func in func_names]
            
            bars1 = ax1.barh(func_names, avg_times, color='lightgreen')
            ax1.set_xlabel('Average Execution Time (ms)', fontweight='bold')
            ax1.set_title('Function Average Execution Times', fontweight='bold')
            
            # Add value labels
            for i, bar in enumerate(bars1):
                width = bar.get_width()
                ax1.text(width, bar.get_y() + bar.get_height()/2,
                        f'{avg_times[i]:.1f}ms', ha='left', va='center')
            
            # Call frequency
            call_counts = [len(self.execution_times[func]) for func in func_names]
            ax2.pie(call_counts, labels=func_names, autopct='%1.1f%%', startangle=90)
            ax2.set_title('Function Call Distribution', fontweight='bold')
            
            # Performance trends (if multiple calls)
            if len(func_names) > 0 and len(self.execution_times[func_names[0]]) > 1:
                for func in func_names[:3]:  # Show trends for top 3 functions
                    times = self.execution_times[func]
                    ax3.plot(range(len(times)), times, marker='o', label=func)
                ax3.set_xlabel('Call Number', fontweight='bold')
                ax3.set_ylabel('Execution Time (ms)', fontweight='bold')
                ax3.set_title('Performance Trends', fontweight='bold')
                ax3.legend()
                ax3.grid(True, alpha=0.3)
            
            # Error rates
            error_rates = []
            for func in func_names:
                total_calls = len(self.execution_times[func])
                errors = self.function_error_count.get(func, 0)
                error_rate = (errors / total_calls) * 100 if total_calls > 0 else 0
                error_rates.append(error_rate)
            
            colors = ['red' if rate > 10 else 'orange' if rate > 5 else 'green' for rate in error_rates]
            bars4 = ax4.bar(func_names, error_rates, color=colors)
            ax4.set_ylabel('Error Rate (%)', fontweight='bold')
            ax4.set_title('Function Error Rates', fontweight='bold')
            ax4.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            file_path = os.path.join(self.insight_dir, f'function_performance_{timestamp}.png')
            plt.savefig(file_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Function performance graph saved to {file_path}")

    def generate_log_summary(self):
        """Enhanced log summary with comprehensive system information"""
        # System information
        environment_info = {
            "Session ID": self.session_id,
            "Logger Name": self.name,
            "Version": __version__,
            "Python Version": platform.python_version(),
            "Operating System": f"{platform.system()} {platform.release()}",
            "Machine": platform.machine(),
            "Processor": platform.processor() or "Unknown",
            "CPU Cores": psutil.cpu_count(logical=False),
            "CPU Threads": psutil.cpu_count(logical=True),
            "Total Memory": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            "Available Memory": f"{psutil.virtual_memory().available / (1024**3):.2f} GB",
            "Disk Usage": f"{psutil.disk_usage('/').percent:.1f}%",
        }
        
        # Runtime information
        runtime_info = {
            "Start Time": self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "Current Time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Uptime": str(datetime.datetime.now() - self.start_time),
            "Total Log Entries": sum(self.error_count.values()),
            "Functions Monitored": len(self.execution_times),
            "Security Events": len(self.security_events),
            "Custom Metrics": len(self.custom_metrics),
        }
        
        # Performance summary
        if self.cpu_usage and self.memory_usage:
            cpu_values = [item['value'] for item in self.cpu_usage]
            mem_values = [item['value'] for item in self.memory_usage]
            
            performance_info = {
                "Avg CPU Usage": f"{safe_mean(cpu_values):.1f}%",
                "Peak CPU Usage": f"{max(cpu_values):.1f}%",
                "Avg Memory Usage": f"{safe_mean(mem_values):.1f}%",
                "Peak Memory Usage": f"{max(mem_values):.1f}%",
            }
        else:
            performance_info = {"Performance Monitoring": "Not Available"}
        
        # Create comprehensive table
        all_info = [("=== SYSTEM INFORMATION ===", "")]
        all_info.extend([(k, v) for k, v in environment_info.items()])
        all_info.append(("=== RUNTIME INFORMATION ===", ""))
        all_info.extend([(k, v) for k, v in runtime_info.items()])
        all_info.append(("=== PERFORMANCE SUMMARY ===", ""))
        all_info.extend([(k, v) for k, v in performance_info.items()])
        
        if self.error_count:
            all_info.append(("=== LOG BREAKDOWN ===", ""))
            all_info.extend([(f"{level} Logs", count) for level, count in self.error_count.items()])
        
        # Anomalies section
        anomalies = self.detect_anomalies()
        if anomalies:
            all_info.append(("=== DETECTED ANOMALIES ===", ""))
            for i, anomaly in enumerate(anomalies, 1):
                all_info.append((f"Anomaly {i}", anomaly))
        
        summary_table = tabulate(all_info, headers=["Metric", "Value"], 
                               tablefmt="fancy_grid", numalign="left")
        
        return summary_table

    def generate_advanced_report(self):
        """Generate comprehensive analysis report"""
        report_data = {
            'executive_summary': {
                'session_id': self.session_id,
                'total_runtime': str(datetime.datetime.now() - self.start_time),
                'health_score': self._calculate_health_score(),
                'recommendation_count': len(self._generate_recommendations())
            },
            'performance_analysis': self.generate_performance_report(),
            'system_health': {
                'anomalies': self.detect_anomalies(),
                'recommendations': self._generate_recommendations(),
                'bottlenecks': self._identify_bottlenecks()
            },
            'security_summary': {
                'total_events': len(self.security_events),
                'high_severity': len([e for e in self.security_events if e['severity'] == 'HIGH']),
                'recent_events': self.security_events[-5:] if self.security_events else []
            }
        }
        
        return report_data

    def _calculate_health_score(self):
        """Calculate overall system health score (0-100)"""
        score = 100
        
        # Deduct for high error rates
        total_logs = sum(self.error_count.values())
        if total_logs > 0:
            error_rate = (self.error_count.get('ERROR', 0) + self.error_count.get('CRITICAL', 0)) / total_logs
            score -= min(error_rate * 50, 30)  # Max 30 point deduction
        
        # Deduct for high resource usage
        if self.cpu_usage:
            avg_cpu = safe_mean([item['value'] for item in self.cpu_usage])
            if avg_cpu > 80:
                score -= min((avg_cpu - 80) * 2, 20)
        
        if self.memory_usage:
            avg_memory = safe_mean([item['value'] for item in self.memory_usage])
            if avg_memory > 85:
                score -= min((avg_memory - 85) * 3, 25)
        
        # Deduct for security events
        high_severity_events = len([e for e in self.security_events if e['severity'] == 'HIGH'])
        score -= min(high_severity_events * 5, 15)
        
        return max(0, score)

    def _generate_recommendations(self):
        """Generate performance and optimization recommendations"""
        recommendations = []
        
        # Function performance recommendations
        for func_name, times in self.execution_times.items():
            if len(times) > 5:  # Only analyze functions with multiple calls
                avg_time = safe_mean(times)
                std_dev = safe_std(times)
                
                if avg_time > 1000:  # Slow functions (>1s)
                    recommendations.append({
                        'category': 'Performance',
                        'severity': 'Medium',
                        'message': f"Function '{func_name}' has high average execution time ({avg_time:.1f}ms)",
                        'suggestion': "Consider optimizing algorithm or caching results"
                    })
                
                if std_dev > avg_time * 0.5:  # High variability
                    recommendations.append({
                        'category': 'Performance',
                        'severity': 'Low',
                        'message': f"Function '{func_name}' has inconsistent execution times",
                        'suggestion': "Review for conditional logic that might cause timing variations"
                    })
        
        # Resource usage recommendations
        if self.cpu_usage:
            avg_cpu = safe_mean([item['value'] for item in self.cpu_usage])
            if avg_cpu > 70:
                recommendations.append({
                    'category': 'System',
                    'severity': 'High' if avg_cpu > 90 else 'Medium',
                    'message': f"High average CPU usage ({avg_cpu:.1f}%)",
                    'suggestion': "Consider optimizing CPU-intensive operations or scaling resources"
                })
        
        if self.memory_usage:
            avg_memory = safe_mean([item['value'] for item in self.memory_usage])
            if avg_memory > 80:
                recommendations.append({
                    'category': 'System',
                    'severity': 'High' if avg_memory > 95 else 'Medium',
                    'message': f"High average memory usage ({avg_memory:.1f}%)",
                    'suggestion': "Review memory usage patterns and consider garbage collection optimization"
                })
        
        # Error rate recommendations
        total_logs = sum(self.error_count.values())
        if total_logs > 0:
            error_rate = (self.error_count.get('ERROR', 0) + self.error_count.get('CRITICAL', 0)) / total_logs
            if error_rate > 0.1:  # >10% error rate
                recommendations.append({
                    'category': 'Reliability',
                    'severity': 'High',
                    'message': f"High error rate ({error_rate*100:.1f}%)",
                    'suggestion': "Review error handling and implement better validation"
                })
        
        return recommendations

    def _identify_bottlenecks(self):
        """Identify performance bottlenecks"""
        bottlenecks = []
        
        if self.execution_times:
            # Find slowest functions
            avg_times = {func: safe_mean(times) for func, times in self.execution_times.items()}
            slowest_funcs = sorted(avg_times.items(), key=lambda x: x[1], reverse=True)[:3]
            
            for func_name, avg_time in slowest_funcs:
                if avg_time > 100:  # Functions taking more than 100ms
                    bottlenecks.append({
                        'type': 'Function Performance',
                        'function': func_name,
                        'avg_time': avg_time,
                        'total_time': sum(self.execution_times[func_name]),
                        'call_count': len(self.execution_times[func_name])
                    })
        
        return bottlenecks

    def view_insights(self, detailed=True, export_format=None, create_dashboard=False):
        """Enhanced insights viewer with comprehensive analysis and export options"""
        print(f"\n{colored('🔍 InsightLog Analysis Dashboard', 'cyan', attrs=['bold'])}")
        print(f"{colored('=' * 60, 'cyan')}")
        print(f"{colored(f'Logger: {self.name} | Session: {self.session_id} | Version: {__version__}', 'white')}")
        print(f"{colored('=' * 60, 'cyan')}\n")
        
        # Health Score Display
        health_score = self._calculate_health_score()
        health_color = 'green' if health_score >= 80 else 'yellow' if health_score >= 60 else 'red'
        print(f"{colored(f'🏥 System Health Score: {health_score:.1f}/100', health_color, attrs=['bold'])}\n")
        
        # Quick Stats
        total_logs = sum(self.error_count.values())
        uptime = datetime.datetime.now() - self.start_time
        
        quick_stats = [
            ["📊 Total Log Entries", total_logs],
            ["⏱️ Uptime", str(uptime).split('.')[0]],
            ["🔧 Functions Monitored", len(self.execution_times)],
            ["🔒 Security Events", len(self.security_events)],
            ["📈 Custom Metrics", len(self.custom_metrics)]
        ]
        
        print(colored("📋 Quick Statistics:", 'magenta', attrs=['bold']))
        print(tabulate(quick_stats, tablefmt="simple", numalign="right"))
        print()
        
        # Detect anomalies
        anomalies = self.detect_anomalies()
        recommendations = self._generate_recommendations()
        
        # Generate all graph types
        if self.error_count or self.execution_times:
            print(colored("📊 Generating visualizations...", 'yellow'))
            self.draw_and_save_graph("all")
        
        if detailed:
            # Detailed Summary
            summary = self.generate_log_summary()
            print(colored('📋 Detailed System Summary:', 'magenta', attrs=['bold']))
            print(summary)
            print()
            
            # Performance Analysis
            if self.execution_times:
                print(colored('⚡ Function Performance Analysis:', 'green', attrs=['bold']))
                func_stats = self.get_function_statistics()
                
                perf_table = []
                for func_name, stats in func_stats.items():
                    perf_table.append([
                        func_name,
                        stats['call_count'],
                        f"{stats['avg_time']:.2f}ms",
                        f"{stats['min_time']:.2f}ms",
                        f"{stats['max_time']:.2f}ms",
                        f"{stats['success_rate']:.1f}%"
                    ])
                
                headers = ["Function", "Calls", "Avg Time", "Min Time", "Max Time", "Success Rate"]
                print(tabulate(perf_table, headers=headers, tablefmt="fancy_grid", floatfmt=".2f"))
                print()
            
            # System Resource Usage
            if self.cpu_usage and self.memory_usage:
                print(colored('💻 System Resource Analysis:', 'blue', attrs=['bold']))
                cpu_values = [item['value'] for item in self.cpu_usage]
                mem_values = [item['value'] for item in self.memory_usage]
                
                resource_stats = [
                    ["CPU Usage - Average", f"{safe_mean(cpu_values):.1f}%"],
                    ["CPU Usage - Peak", f"{max(cpu_values):.1f}%"],
                    ["Memory Usage - Average", f"{safe_mean(mem_values):.1f}%"],
                    ["Memory Usage - Peak", f"{max(mem_values):.1f}%"],
                    ["Monitoring Duration", f"{len(cpu_values) * 5} seconds"]
                ]
                
                print(tabulate(resource_stats, headers=["Metric", "Value"], tablefmt="simple"))
                print()
            
            # Anomaly Detection
            anomalies = self.detect_anomalies()
            if anomalies:
                print(colored('🚨 Detected Anomalies:', 'red', attrs=['bold']))
                for i, anomaly in enumerate(anomalies, 1):
                    print(f"  {i}. {colored(anomaly, 'red')}")
                print()
            
            # Recommendations
            if recommendations:
                print(colored('💡 Optimization Recommendations:', 'yellow', attrs=['bold']))
                for rec in recommendations:
                    severity_color = {'High': 'red', 'Medium': 'yellow', 'Low': 'cyan'}.get(rec['severity'], 'white')
                    print(f"  • {colored(f'[{rec["severity"]}]', severity_color, attrs=['bold'])} "
                          f"{rec['message']}")
                    print(f"    💭 {rec['suggestion']}")
                print()
            
            # Security Events
            if self.security_events:
                print(colored('🔒 Recent Security Events:', 'red', attrs=['bold']))
                recent_events = self.security_events[-5:]
                for event in recent_events:
                    severity_color = {'HIGH': 'red', 'MEDIUM': 'yellow', 'LOW': 'cyan'}.get(event['severity'], 'white')
                    timestamp_str = event['timestamp'].strftime('%H:%M:%S')
                    severity_str = f"[{event['severity']}]"
                    print(f"  • {colored(timestamp_str, 'white')} "
                          f"{colored(severity_str, severity_color, attrs=['bold'])} "
                          f"{event['event_type']}: {event['description']}")
                print()
        
        # Export options
        if export_format:
            print(colored(f"📤 Exporting data in {export_format.upper()} format...", 'yellow'))
            export_path = self.export_data(export_format, include_raw_data=detailed)
            print(colored(f"✅ Data exported to: {export_path}", 'green'))
            print()
        
        # Dashboard creation
        if create_dashboard:
            print(colored("🌐 Creating HTML dashboard...", 'yellow'))
            dashboard_path = self.create_dashboard_html()
            print(colored(f"✅ Dashboard created: {dashboard_path}", 'green'))
            print()
        
        # Final summary
        print(colored('🎯 Session Summary:', 'cyan', attrs=['bold']))
        print(f"  • Health Score: {colored(f'{health_score:.1f}/100', health_color, attrs=['bold'])}")
        print(f"  • Total Runtime: {colored(str(uptime).split('.')[0], 'white', attrs=['bold'])}")
        print(f"  • Data Points Collected: {colored(str(total_logs + len(self.cpu_usage) + len(self.custom_metrics)), 'white', attrs=['bold'])}")
        
        if anomalies:
            print(f"  • Anomalies Detected: {colored(str(len(anomalies)), 'red', attrs=['bold'])}")
        if recommendations:
            print(f"  • Recommendations: {colored(str(len(recommendations)), 'yellow', attrs=['bold'])}")
        
        print(f"\n{colored('Analysis Complete! 🎉', 'green', attrs=['bold'])}")

    def stop_monitoring(self):
        """Stop the monitoring thread and cleanup resources"""
        if hasattr(self, 'monitoring_active'):
            self.monitoring_active = False
            if hasattr(self, 'monitor_thread'):
                self.monitor_thread.join(timeout=1)
        
        if hasattr(self, 'conn'):
            self.conn.close()
        
        self.logger.info("InsightLogger monitoring stopped and resources cleaned up")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup"""
        self.stop_monitoring()
        
        if exc_type:
            self.log_types("CRITICAL", f"Context exit with exception: {exc_type.__name__}: {exc_val}")
            self.log_security_event("EXCEPTION_EXIT", "HIGH", f"Unhandled exception: {exc_type.__name__}")
        
        # Generate final report
        print(f"\n{colored('📊 Final Session Report', 'cyan', attrs=['bold'])}")
        self.view_insights(detailed=False)

# Enhanced utility functions
def monitor_decorator(logger_instance):
    """Decorator factory for monitoring functions with a specific logger instance"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with logger_instance.performance_profile(func.__name__):
                try:
                    result = func(*args, **kwargs)
                    logger_instance.add_custom_metric(f"{func.__name__}_success", 1)
                    return result
                except Exception as e:
                    logger_instance.log_types("ERROR", f"Function {func.__name__} failed: {str(e)}")
                    logger_instance.add_custom_metric(f"{func.__name__}_error", 1)
                    raise
        return wrapper
    return decorator

def secure_log_decorator(logger_instance, mask_patterns=None):
    """Decorator to automatically mask sensitive data in logs"""
    mask_patterns = mask_patterns or [r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b']  # Credit card pattern
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Log function entry with masked arguments
            masked_args = str(args)
            for pattern in mask_patterns:
                import re
                masked_args = re.sub(pattern, "****", masked_args)
            
            logger_instance.log_types("TRACE", f"Entering {func.__name__} with args: {masked_args}")
            
            try:
                result = func(*args, **kwargs)
                logger_instance.log_types("TRACE", f"Exiting {func.__name__} successfully")
                return result
            except Exception as e:
                logger_instance.log_security_event("FUNCTION_EXCEPTION", "MEDIUM", 
                                                 f"Exception in {func.__name__}: {type(e).__name__}")
                raise
        return wrapper
    return decorator

class MetricsCollector:
    """Standalone metrics collector for integration with existing applications"""
    
    def __init__(self, logger_instance):
        self.logger = logger_instance
        self.start_time = time.perf_counter()
        
    def time_operation(self, operation_name):
        """Context manager for timing operations"""
        @contextmanager
        def timer():
            start = time.perf_counter()
            try:
                yield
            finally:
                duration = (time.perf_counter() - start) * 1000
                self.logger.add_custom_metric(f"operation_time_{operation_name}", duration)
        return timer()
    
    def count_event(self, event_name):
        """Increment event counter"""
        self.logger.add_custom_metric(f"event_count_{event_name}", 1)
    
    def gauge_value(self, metric_name, value):
        """Record a gauge metric"""
        self.logger.add_custom_metric(f"gauge_{metric_name}", value)

# Enhanced Main Function to Demonstrate New Features
def main():
    """Comprehensive demonstration of InsightLogger v1.4 features"""
    print(f"{colored('🚀 InsightLogger v1.4 Feature Demonstration', 'cyan', attrs=['bold'])}")
    print(f"{colored('=' * 50, 'cyan')}\n")
    
    try:
        # Initialize with enhanced features
        with InsightLogger(
            name="InsightLogDemo",
            enable_database=True,
            enable_monitoring=True,
            enable_alerts=False,  # Set to True with email config for real alerts
            log_level=logging.INFO
        ) as insight_logger:
            
            print(colored("🔧 Initializing enhanced logger with monitoring...", 'yellow'))
            time.sleep(2)
            
            # Demonstrate function timing with enhanced decorator
            @insight_logger.log_function_time
            def cpu_intensive_task():
                """Simulate CPU intensive work"""
                total = 0
                for i in range(1000000):
                    total += i ** 0.5
                return total
            
            @insight_logger.log_function_time
            def memory_intensive_task():
                """Simulate memory intensive work"""
                large_list = [i for i in range(500000)]
                return sum(large_list)
            
            @insight_logger.log_function_time
            def io_simulation():
                """Simulate I/O operations"""
                time.sleep(1.5)
                return "I/O complete"
            
            # Performance profiling demo
            print(colored("⚡ Demonstrating performance profiling...", 'green'))
            
            with insight_logger.performance_profile("data_processing"):
                result1 = cpu_intensive_task()
                insight_logger.log_types("SUCCESS", f"CPU task completed, result: {result1:.2f}")
            
            with insight_logger.performance_profile("memory_operations"):
                result2 = memory_intensive_task()
                insight_logger.log_types("SUCCESS", f"Memory task completed, result: {result2}")
            
            result3 = io_simulation()
            insight_logger.log_types("INFO", f"I/O task completed: {result3}")
            
            # Custom metrics demonstration
            print(colored("📊 Adding custom metrics...", 'blue'))
            insight_logger.add_custom_metric("user_interactions", 45)
            insight_logger.add_custom_metric("api_requests", 123)
            insight_logger.add_custom_metric("cache_hits", 89)
            insight_logger.add_custom_metric("database_queries", 34)
            
            # API call tracking demo
            insight_logger.track_api_call("/api/users", "GET", 234, 200)
            insight_logger.track_api_call("/api/data", "POST", 445, 201)
            insight_logger.track_api_call("/api/auth", "POST", 156, 401)
            
            # Security event simulation
            print(colored("🔒 Simulating security events...", 'red'))
            insight_logger.log_security_event("LOGIN_ATTEMPT", "LOW", "User login from new IP")
            insight_logger.log_security_event("FAILED_LOGIN", "MEDIUM", "Multiple failed login attempts")
            insight_logger.log_security_event("PRIVILEGE_ESCALATION", "HIGH", "Unauthorized access attempt")
            
            # Comprehensive logging demonstration
            print(colored("📝 Demonstrating enhanced logging features...", 'magenta'))
            
            insight_logger.log_types("INFO", "Application startup completed", emoji=True, bold=True)
            insight_logger.log_types("SUCCESS", "Database connection established", border=True)
            insight_logger.log_types("WARNING", "Cache miss detected", urgent=False)
            insight_logger.log_types("ERROR", "Failed to connect to external API", background=True)
            
            # Contextual logging
            insight_logger.log_with_context(
                "INFO", 
                "User action processed",
                context={"user_id": 12345, "action": "data_export", "ip": "192.168.1.100"},
                tags=["user_activity", "export", "audit"]
            )
            
            # Batch logging demonstration
            batch_logs = [
                {"level": "DEBUG", "message": "Processing batch item 1"},
                {"level": "DEBUG", "message": "Processing batch item 2"},
                {"level": "INFO", "message": "Batch processing completed"},
                ("WARNING", "Some items were skipped during batch processing")
            ]
            insight_logger.batch_log(batch_logs)
            
            # Simulate some errors for demonstration
            try:
                raise ValueError("Simulated error for demonstration")
            except ValueError as e:
                insight_logger.log_types("ERROR", f"Caught exception: {str(e)}")
            
            insight_logger.log_types("CRITICAL", "System overload detected", urgent=True)
            insight_logger.log_types("ALERT", "Unusual activity pattern", background=True)
            insight_logger.log_types("HIGHLIGHT", "Performance milestone reached", header=True)
            
            # Wait for monitoring data to accumulate
            print(colored("⏳ Collecting system metrics...", 'yellow'))
            time.sleep(8)  # Allow monitoring to collect data
            
            # Generate comprehensive insights
            print(colored("\n🔍 Generating comprehensive analysis...", 'cyan'))
            insight_logger.view_insights(detailed=True, create_dashboard=True)
            
            # Export demonstration
            print(colored("📤 Exporting session data...", 'yellow'))
            json_export = insight_logger.export_data("json", include_raw_data=True)
            csv_export = insight_logger.export_data("csv")
            
            # Performance report
            report = insight_logger.generate_advanced_report()
            print(colored(f"\n📋 Advanced Report Generated:", 'green', attrs=['bold']))
            print(f"  • Health Score: {report['executive_summary']['health_score']:.1f}/100")
            print(f"  • Total Runtime: {report['executive_summary']['total_runtime']}")
            print(f"  • Recommendations: {report['executive_summary']['recommendation_count']}")
            
            # Function statistics
            func_stats = insight_logger.get_function_statistics()
            if func_stats:
                print(colored(f"\n⚡ Top Performing Functions:", 'blue', attrs=['bold']))
                sorted_funcs = sorted(func_stats.items(), key=lambda x: x[1]['avg_time'])
                for func_name, stats in sorted_funcs[:3]:
                    print(f"  • {func_name}: {stats['avg_time']:.1f}ms avg, {stats['call_count']} calls")
            
            print(colored(f"\n✨ Demo completed successfully!", 'green', attrs=['bold']))
            print(f"Check the '{insight_logger.insight_dir}' directory for generated files:")
            print(f"  • Graphs and visualizations")
            print(f"  • HTML dashboard")
            print(f"  • SQLite database with detailed logs")
            print(f"  • Exported data files")
    
    except KeyboardInterrupt:
        print(colored("\n⏹️ Demo interrupted by user", 'yellow'))
    except Exception as e:
        print(colored(f"💥 Demo error: {e}", 'red'))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
