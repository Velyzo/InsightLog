# Configuration Guide

Complete guide to configuring InsightLogger for optimal performance and functionality.

## 🔧 Basic Configuration

### Default Configuration

```python
from insightlog import InsightLogger

# Minimal configuration (uses all defaults)
logger = InsightLogger("MyApp")

# Default values:
# - save_log="enabled"
# - log_dir=".insight"
# - log_filename="app.log"
# - max_bytes=1000000 (1MB)
# - backup_count=1
# - log_level=logging.DEBUG
# - enable_database=True
# - enable_monitoring=True
# - enable_alerts=False
```

### Custom Configuration

```python
import logging
from insightlog import InsightLogger

logger = InsightLogger(
    name="ProductionApp",
    save_log="enabled",
    log_dir="./logs",
    log_filename="production.log",
    max_bytes=10000000,  # 10MB
    backup_count=5,
    log_level=logging.INFO,
    enable_database=True,
    enable_monitoring=True,
    enable_alerts=True,
    alert_email="admin@company.com",
    smtp_server="smtp.company.com",
    smtp_port=587,
    smtp_user="alerts@company.com",
    smtp_password="secure_password"
)
```

## 📂 File System Configuration

### Log Directory Structure

```
project_root/
├── .insight/                    # Default insight directory
│   ├── app.log                 # Main log file
│   ├── app.log.1               # Backup log file
│   ├── insights_session.db     # SQLite database
│   ├── performance_chart.png   # Generated charts
│   ├── dashboard.html          # HTML dashboard
│   └── exports/                # Exported data
│       ├── session_data.json
│       └── analytics.csv
├── logs/                       # Custom log directory
│   ├── production.log
│   └── debug.log
└── your_app.py
```

### Custom Directories

```python
# Custom log directory
logger = InsightLogger(
    name="MyApp",
    log_dir="/var/log/myapp",        # Linux/Mac
    # log_dir="C:\\Logs\\MyApp",     # Windows
    log_filename="application.log"
)

# Relative path
logger = InsightLogger(
    name="MyApp",
    log_dir="./application_logs",
    log_filename="app.log"
)

# Disable file logging
logger = InsightLogger(
    name="MyApp",
    save_log="disabled"
)
```

### Log Rotation Configuration

```python
logger = InsightLogger(
    name="HighVolumeApp",
    max_bytes=50000000,      # 50MB per file
    backup_count=10,         # Keep 10 backup files
    log_filename="app.log"
)

# This creates:
# app.log         (current)
# app.log.1       (most recent backup)
# app.log.2
# ...
# app.log.10      (oldest backup)
```

## 🗄️ Database Configuration

### SQLite Configuration (Default)

```python
# Enable database with defaults
logger = InsightLogger(
    name="MyApp",
    enable_database=True  # Creates .insight/insights_session.db
)

# Custom database location
logger = InsightLogger(
    name="MyApp",
    enable_database=True,
    log_dir="./database"  # Database will be in ./database/insights_session.db
)
```

### Database Schema

The SQLite database automatically creates these tables:

```sql
-- Main logs table
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    level TEXT,
    message TEXT,
    function_name TEXT,
    execution_time REAL,
    memory_usage REAL,
    context TEXT,  -- JSON string
    tags TEXT,     -- JSON array
    session_id TEXT
);

-- Performance metrics table
CREATE TABLE performance_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    function_name TEXT,
    execution_time REAL,
    memory_usage REAL,
    cpu_usage REAL,
    session_id TEXT
);

-- System metrics table
CREATE TABLE system_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    cpu_percent REAL,
    memory_percent REAL,
    disk_usage REAL,
    network_io_sent INTEGER,
    network_io_recv INTEGER,
    session_id TEXT
);

-- Security events table
CREATE TABLE security_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    event_type TEXT,
    severity TEXT,
    description TEXT,
    additional_data TEXT,  -- JSON string
    session_id TEXT
);

-- Custom metrics table
CREATE TABLE custom_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    metric_name TEXT,
    metric_value REAL,
    session_id TEXT
);
```

### Disable Database

```python
# Disable database logging
logger = InsightLogger(
    name="LightweightApp",
    enable_database=False
)
```

## 📊 Monitoring Configuration

### System Monitoring

```python
# Enable system monitoring (default)
logger = InsightLogger(
    name="MonitoredApp",
    enable_monitoring=True
)

# Disable system monitoring for lightweight usage
logger = InsightLogger(
    name="LightApp",
    enable_monitoring=False
)
```

### Monitoring Intervals

The monitoring system collects metrics at these intervals:
- **CPU Usage**: Every 1 second
- **Memory Usage**: Every 1 second  
- **Network I/O**: Every 5 seconds
- **Disk Usage**: Every 30 seconds

### Custom Monitoring Configuration

```python
# After initialization, you can configure monitoring
logger = InsightLogger("MyApp")

# Set custom alert thresholds
logger.alert_thresholds = {
    'cpu_usage': 85,        # Alert when CPU > 85%
    'memory_usage': 90,     # Alert when memory > 90%
    'error_rate': 5,        # Alert when error rate > 5%
    'response_time': 2000   # Alert when response time > 2000ms
}
```

## 📧 Email Alert Configuration

### SMTP Configuration

```python
logger = InsightLogger(
    name="ProductionApp",
    enable_alerts=True,
    alert_email="admin@company.com",
    smtp_server="smtp.gmail.com",      # Gmail SMTP
    smtp_port=587,
    smtp_user="alerts@company.com",
    smtp_password="app_specific_password"
)
```

### Multiple Recipients

```python
# Multiple email recipients
logger = InsightLogger(
    name="CriticalApp",
    enable_alerts=True,
    alert_email="admin@company.com,dev@company.com,ops@company.com",
    smtp_server="smtp.company.com",
    smtp_port=587,
    smtp_user="alerts@company.com",
    smtp_password="secure_password"
)
```

### Common SMTP Configurations

#### Gmail
```python
smtp_config = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_user": "your_email@gmail.com",
    "smtp_password": "app_specific_password"  # Use app password, not regular password
}
```

#### Outlook/Hotmail
```python
smtp_config = {
    "smtp_server": "smtp-mail.outlook.com",
    "smtp_port": 587,
    "smtp_user": "your_email@outlook.com",
    "smtp_password": "your_password"
}
```

#### Corporate Exchange
```python
smtp_config = {
    "smtp_server": "mail.company.com",
    "smtp_port": 587,  # or 25, 465
    "smtp_user": "username@company.com",
    "smtp_password": "password"
}
```

### Alert Configuration

```python
# Configure when alerts are sent
logger.alert_thresholds = {
    'cpu_usage': 80,         # CPU usage > 80%
    'memory_usage': 85,      # Memory usage > 85%
    'error_rate': 10,        # Error rate > 10%
    'response_time': 5000,   # Response time > 5 seconds
    'disk_usage': 90,        # Disk usage > 90%
    'failed_logins': 5       # Failed logins > 5 in 1 minute
}
```

## 🎨 Logging Level Configuration

### Standard Python Logging Levels

```python
import logging

# Configure different log levels
logger_debug = InsightLogger("DebugApp", log_level=logging.DEBUG)     # All messages
logger_info = InsightLogger("InfoApp", log_level=logging.INFO)        # INFO and above
logger_warning = InsightLogger("WarnApp", log_level=logging.WARNING)  # WARNING and above
logger_error = InsightLogger("ErrorApp", log_level=logging.ERROR)     # ERROR and above
logger_critical = InsightLogger("CritApp", log_level=logging.CRITICAL) # CRITICAL only
```

### Level Hierarchy

```
CRITICAL (50) - Most severe
ERROR    (40)
WARNING  (30)
INFO     (20)
DEBUG    (10) - Most verbose
```

### Production vs Development

```python
import os
import logging

# Determine log level based on environment
log_level = logging.DEBUG if os.getenv('ENV') == 'development' else logging.INFO

logger = InsightLogger(
    name="MyApp",
    log_level=log_level,
    enable_monitoring=True,
    enable_database=True
)
```

## 🔧 Advanced Configuration

### Environment Variables

```python
import os
from insightlog import InsightLogger

# Configure using environment variables
logger = InsightLogger(
    name=os.getenv('APP_NAME', 'DefaultApp'),
    log_dir=os.getenv('LOG_DIR', '.insight'),
    log_filename=os.getenv('LOG_FILENAME', 'app.log'),
    enable_database=os.getenv('ENABLE_DB', 'true').lower() == 'true',
    enable_monitoring=os.getenv('ENABLE_MONITORING', 'true').lower() == 'true',
    enable_alerts=os.getenv('ENABLE_ALERTS', 'false').lower() == 'true',
    alert_email=os.getenv('ALERT_EMAIL'),
    smtp_server=os.getenv('SMTP_SERVER'),
    smtp_user=os.getenv('SMTP_USER'),
    smtp_password=os.getenv('SMTP_PASSWORD')
)
```

### Configuration File

```python
# config.json
{
    "logger": {
        "name": "ProductionApp",
        "log_dir": "./logs",
        "log_filename": "production.log",
        "max_bytes": 10000000,
        "backup_count": 5,
        "log_level": "INFO",
        "enable_database": true,
        "enable_monitoring": true,
        "enable_alerts": true,
        "alert_email": "admin@company.com",
        "smtp_server": "smtp.company.com",
        "smtp_port": 587,
        "smtp_user": "alerts@company.com"
    }
}
```

```python
import json
import logging
from insightlog import InsightLogger

# Load configuration from file
with open('config.json', 'r') as f:
    config = json.load(f)

logger_config = config['logger']

# Convert log level string to constant
log_level_map = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

logger = InsightLogger(
    name=logger_config['name'],
    log_dir=logger_config['log_dir'],
    log_filename=logger_config['log_filename'],
    max_bytes=logger_config['max_bytes'],
    backup_count=logger_config['backup_count'],
    log_level=log_level_map[logger_config['log_level']],
    enable_database=logger_config['enable_database'],
    enable_monitoring=logger_config['enable_monitoring'],
    enable_alerts=logger_config['enable_alerts'],
    alert_email=logger_config['alert_email'],
    smtp_server=logger_config['smtp_server'],
    smtp_port=logger_config['smtp_port'],
    smtp_user=logger_config['smtp_user'],
    smtp_password=os.getenv('SMTP_PASSWORD')  # Keep passwords in env vars
)
```

## 🐳 Docker Configuration

### Dockerfile Configuration

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Create log directory
RUN mkdir -p /app/logs

# Environment variables for configuration
ENV APP_NAME=DockerApp
ENV LOG_DIR=/app/logs
ENV LOG_FILENAME=docker.log
ENV ENABLE_DB=true
ENV ENABLE_MONITORING=true
ENV ENABLE_ALERTS=false

# Run application
CMD ["python", "app.py"]
```

### Docker Compose Configuration

```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      - APP_NAME=DockerApp
      - LOG_DIR=/app/logs
      - LOG_FILENAME=application.log
      - ENABLE_DB=true
      - ENABLE_MONITORING=true
      - ENABLE_ALERTS=true
      - ALERT_EMAIL=admin@company.com
      - SMTP_SERVER=smtp.company.com
      - SMTP_USER=alerts@company.com
      - SMTP_PASSWORD_FILE=/run/secrets/smtp_password
    volumes:
      - ./logs:/app/logs
      - ./insights:/app/.insight
    secrets:
      - smtp_password

secrets:
  smtp_password:
    file: ./secrets/smtp_password.txt
```

## ☁️ Cloud Configuration

### AWS Configuration

```python
import boto3
from insightlog import InsightLogger

# Configure for AWS deployment
logger = InsightLogger(
    name="AWSApp",
    log_dir="/var/log/myapp",
    enable_database=True,
    enable_monitoring=True,
    enable_alerts=True,
    alert_email="alerts@company.com",
    smtp_server="email-smtp.us-east-1.amazonaws.com",  # AWS SES
    smtp_port=587,
    smtp_user=os.getenv('AWS_SES_USER'),
    smtp_password=os.getenv('AWS_SES_PASSWORD')
)
```

### Azure Configuration

```python
from insightlog import InsightLogger

# Configure for Azure deployment
logger = InsightLogger(
    name="AzureApp",
    log_dir="/home/LogFiles",  # Azure App Service log directory
    enable_database=True,
    enable_monitoring=True,
    enable_alerts=True,
    alert_email="alerts@company.com",
    smtp_server="smtp-mail.outlook.com",
    smtp_port=587,
    smtp_user=os.getenv('AZURE_EMAIL_USER'),
    smtp_password=os.getenv('AZURE_EMAIL_PASSWORD')
)
```

### Google Cloud Configuration

```python
from insightlog import InsightLogger

# Configure for Google Cloud deployment
logger = InsightLogger(
    name="GCPApp",
    log_dir="/var/log/app",
    enable_database=True,
    enable_monitoring=True,
    enable_alerts=True,
    alert_email="alerts@company.com",
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    smtp_user=os.getenv('GMAIL_USER'),
    smtp_password=os.getenv('GMAIL_APP_PASSWORD')
)
```

## 🔄 Runtime Configuration Updates

### Dynamic Configuration Changes

```python
from insightlog import InsightLogger

logger = InsightLogger("MyApp")

# Update configuration at runtime
logger.update_config(
    log_level=logging.WARNING,  # Change log level
    enable_alerts=True,         # Enable alerts
    alert_email="new_admin@company.com"
)

# Update alert thresholds
logger.alert_thresholds['cpu_usage'] = 75
logger.alert_thresholds['memory_usage'] = 80

# Add new custom metrics
logger.add_custom_metric("new_metric", 42.0)
```

### Configuration Validation

```python
def validate_config(logger_config):
    """Validate logger configuration"""
    required_fields = ['name']
    
    for field in required_fields:
        if field not in logger_config:
            raise ValueError(f"Missing required field: {field}")
    
    if logger_config.get('enable_alerts') and not logger_config.get('alert_email'):
        raise ValueError("alert_email required when enable_alerts=True")
    
    if logger_config.get('max_bytes', 0) <= 0:
        raise ValueError("max_bytes must be positive")
    
    return True

# Use validation
config = {
    'name': 'MyApp',
    'enable_alerts': True,
    'alert_email': 'admin@company.com'
}

validate_config(config)
logger = InsightLogger(**config)
```

## 🎯 Configuration Examples by Use Case

### Development Environment

```python
import logging
from insightlog import InsightLogger

dev_logger = InsightLogger(
    name="DevApp",
    log_level=logging.DEBUG,      # Verbose logging
    enable_database=True,         # Store all logs
    enable_monitoring=True,       # Monitor during development
    enable_alerts=False,          # No email alerts
    max_bytes=1000000,           # 1MB files (small for dev)
    backup_count=2               # Keep fewer backups
)
```

### Production Environment

```python
import logging
from insightlog import InsightLogger

prod_logger = InsightLogger(
    name="ProdApp",
    log_level=logging.INFO,       # Less verbose
    log_dir="/var/log/myapp",    # Standard location
    enable_database=True,         # Store logs
    enable_monitoring=True,       # Monitor production
    enable_alerts=True,          # Email alerts
    alert_email="ops@company.com",
    smtp_server="smtp.company.com",
    smtp_user="alerts@company.com",
    smtp_password=os.getenv('SMTP_PASSWORD'),
    max_bytes=50000000,          # 50MB files
    backup_count=10              # Keep more backups
)
```

### Testing Environment

```python
import logging
from insightlog import InsightLogger

test_logger = InsightLogger(
    name="TestApp",
    log_level=logging.ERROR,      # Only errors
    save_log="disabled",          # No file logging
    enable_database=False,        # No database
    enable_monitoring=False,      # No monitoring
    enable_alerts=False          # No alerts
)
```

### High-Performance Environment

```python
import logging
from insightlog import InsightLogger

perf_logger = InsightLogger(
    name="HighPerfApp",
    log_level=logging.WARNING,    # Minimal logging
    enable_database=False,        # No database overhead
    enable_monitoring=True,       # Monitor performance
    enable_alerts=True,          # Critical alerts only
    max_bytes=100000000,         # Large files
    backup_count=3               # Minimal backups
)
```

## 🛠️ Troubleshooting Configuration

### Common Issues

#### Permission Errors
```python
# Solution: Use user directory or check permissions
import os
from pathlib import Path

log_dir = os.path.join(Path.home(), 'app_logs')
logger = InsightLogger("MyApp", log_dir=log_dir)
```

#### SMTP Authentication Errors
```python
# Solution: Use app-specific passwords
logger = InsightLogger(
    name="MyApp",
    enable_alerts=True,
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    smtp_user="your_email@gmail.com",
    smtp_password="app_specific_password"  # Not your regular password
)
```

#### Database Lock Errors
```python
# Solution: Disable database for multi-threaded apps or use file locking
logger = InsightLogger(
    name="ThreadedApp",
    enable_database=False  # Avoid SQLite issues in multi-threaded apps
)
```

### Configuration Validation

```python
def test_configuration():
    """Test logger configuration"""
    try:
        logger = InsightLogger("TestConfig")
        logger.log_types("INFO", "Configuration test")
        
        # Test database
        if logger.enable_database:
            logger.query_logs(limit=1)
            print("✅ Database configuration OK")
        
        # Test monitoring
        if logger.enable_monitoring:
            print("✅ Monitoring configuration OK")
        
        # Test alerts (if configured)
        if logger.enable_alerts and logger.smtp_config:
            print("✅ Alert configuration OK")
        
        logger.stop_monitoring()
        print("✅ All configuration tests passed")
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")

test_configuration()
```

---

## 📚 Related Documentation

- [Installation Guide](installation.md)
- [API Reference](api-reference.md)
- [Best Practices](best-practices.md)
- [Troubleshooting](troubleshooting.md)

---

**Perfect configuration leads to perfect logging!** ⚙️✨

Configure InsightLogger to match your exact needs and environment for optimal performance and functionality.
