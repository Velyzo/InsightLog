# InsightLogger

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/insightlog.svg)](https://pypi.org/project/insightlog/)

A comprehensive logging and monitoring library for Python applications with performance tracking, system monitoring, and analytics capabilities.

## Installation

```bash
pip install insightlog
```

## Quick Start

```python
from insightlog import InsightLogger

# Basic setup
logger = InsightLogger(name="MyApp")

# Log messages
logger.log_types("INFO", "Application started")
logger.log_types("ERROR", "Something went wrong")

# Track function performance
@logger.log_function_time
def my_function():
    # Your code here
    pass

# View insights
logger.view_insights()
```

## Features

### Core Logging
- Multiple log levels (INFO, DEBUG, ERROR, SUCCESS, WARNING, CRITICAL, etc.)
- Colored console output
- File logging with rotation
- Contextual logging with metadata and tags

### Performance Monitoring
- Function execution time tracking
- Memory usage monitoring
- System resource monitoring (CPU, memory, network)
- Custom metrics tracking

### Analytics & Reporting
- Performance profiling and bottleneck identification
- Anomaly detection
- Health scoring
- HTML dashboard generation
- Data export (JSON, CSV)

### Advanced Features
- Database logging (SQLite)
- Email alerts for critical events
- Security event logging
- Plugin system for extensibility

## Configuration

### Basic Configuration

```python
logger = InsightLogger(
    name="MyApp",
    enable_monitoring=True,    # Enable system monitoring
    enable_database=True,      # Enable database logging
    enable_alerts=False        # Disable email alerts
)
```

### Customizable Tracking Options

You can selectively enable/disable specific tracking features:

```python
logger = InsightLogger(
    name="MyApp",
    # Core settings
    save_log="enabled",           # File logging: "enabled" or "disabled"
    log_level=logging.INFO,       # Log level
    
    # Monitoring options
    enable_monitoring=True,       # System resource monitoring
    enable_database=True,         # Database logging
    enable_alerts=False,          # Email alerts
    
    # File settings
    log_dir=".insight",          # Log directory
    max_bytes=1000000,           # Max log file size
    backup_count=3               # Number of backup files
)
```

### Alert Configuration

```python
# Enable email alerts
logger = InsightLogger(
    name="MyApp",
    enable_alerts=True,
    alert_email="admin@company.com",
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    smtp_user="alerts@company.com",
    smtp_password="your_password"
)

# Customize alert thresholds
logger.alert_thresholds = {
    'cpu_usage': 80,        # CPU percentage
    'memory_usage': 85,     # Memory percentage
    'error_rate': 10,       # Error rate percentage
    'response_time': 5000   # Response time in ms
}
```

## Usage Examples

### Performance Tracking

```python
# Method 1: Decorator
@logger.log_function_time
def process_data():
    # Your code here
    pass

# Method 2: Context manager
with logger.performance_profile("data_processing"):
    # Your code here
    pass
```

### Custom Metrics

```python
# Track application-specific metrics
logger.add_custom_metric("active_users", 150)
logger.add_custom_metric("cache_hit_rate", 0.95)

# Track API calls
logger.track_api_call("/api/users", "GET", response_time=234, status_code=200)
```

### Security Logging

```python
logger.log_security_event("LOGIN_ATTEMPT", "MEDIUM", "Failed login attempt")
```

### Batch Logging

```python
logs = [
    {"level": "INFO", "message": "Processing item 1"},
    {"level": "INFO", "message": "Processing item 2"},
    ("SUCCESS", "Batch completed")
]
logger.batch_log(logs)
```

### Contextual Logging

```python
logger.log_with_context(
    "INFO",
    "User action performed",
    context={"user_id": 12345, "action": "file_upload"},
    tags=["user_activity", "audit"]
)
```

## Reports and Dashboards

### Generate Reports

```python
# View insights in console
logger.view_insights(detailed=True)

# Create HTML dashboard
logger.view_insights(create_dashboard=True)

# Export data
logger.export_data("json", include_raw_data=True)
logger.export_data("csv")
```

### Output Files

InsightLogger creates files in the `.insight` directory:

```
.insight/
├── app.log                           # Log file
├── insights_[session].db             # SQLite database
├── dashboard_[session].html          # HTML dashboard
├── log_frequency_[timestamp].png     # Charts
├── system_metrics_[timestamp].png
└── function_performance_[timestamp].png
```

## Framework Integration

### Flask Example

```python
from flask import Flask
from insightlog import InsightLogger

app = Flask(__name__)
logger = InsightLogger("FlaskApp", enable_monitoring=True)

@app.route('/api/data')
@logger.log_function_time
def get_data():
    logger.track_api_call("/api/data", "GET", response_time=150, status_code=200)
    return {"data": "example"}
```

## Documentation

For detailed documentation, examples, and advanced usage, see the [docs](docs/) directory.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests to our GitHub repository.

## Support

- GitHub Issues: [Report bugs](https://github.com/Velyzo/InsightLog/issues)
- Documentation: [docs/](docs/)
- PyPI: [https://pypi.org/project/insightlog/](https://pypi.org/project/insightlog/)
