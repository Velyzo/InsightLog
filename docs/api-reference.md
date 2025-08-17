# API Reference

Complete API documentation for InsightLogger with all classes, methods, and parameters.

## 🏗️ Core Classes

### InsightLogger

The main logger class providing comprehensive logging and monitoring capabilities.

```python
class InsightLogger:
    """
    Advanced logging utility with comprehensive monitoring, analytics, and reporting capabilities.
    """
```

#### Constructor

```python
def __init__(self, 
             name: str,
             save_log: str = "enabled",
             log_dir: str = ".insight",
             log_filename: str = "app.log",
             max_bytes: int = 1000000,
             backup_count: int = 1,
             log_level: int = logging.DEBUG,
             enable_database: bool = True,
             enable_monitoring: bool = True,
             enable_alerts: bool = False,
             alert_email: str = None,
             smtp_server: str = None,
             smtp_port: int = 587,
             smtp_user: str = None,
             smtp_password: str = None):
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | Required | Logger instance name |
| `save_log` | `str` | `"enabled"` | Enable/disable file logging |
| `log_dir` | `str` | `".insight"` | Directory for log files |
| `log_filename` | `str` | `"app.log"` | Log file name |
| `max_bytes` | `int` | `1000000` | Maximum log file size in bytes |
| `backup_count` | `int` | `1` | Number of backup log files to keep |
| `log_level` | `int` | `logging.DEBUG` | Minimum logging level |
| `enable_database` | `bool` | `True` | Enable SQLite database logging |
| `enable_monitoring` | `bool` | `True` | Enable system monitoring |
| `enable_alerts` | `bool` | `False` | Enable email alerts |
| `alert_email` | `str` | `None` | Email address for alerts |
| `smtp_server` | `str` | `None` | SMTP server for email alerts |
| `smtp_port` | `int` | `587` | SMTP server port |
| `smtp_user` | `str` | `None` | SMTP username |
| `smtp_password` | `str` | `None` | SMTP password |

## 📝 Logging Methods

### log_types()

Primary logging method with enhanced formatting options.

```python
def log_types(self, 
              level: str, 
              text: str, 
              bold: bool = False, 
              background: str = None, 
              border: bool = False, 
              header: bool = False, 
              underline: bool = False, 
              urgent: bool = False, 
              emoji: bool = True) -> None:
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `level` | `str` | Required | Log level: INFO, SUCCESS, WARNING, ERROR, DEBUG, CRITICAL, ALERT, TRACE, HIGHLIGHT, FAILURE |
| `text` | `str` | Required | Message to log |
| `bold` | `bool` | `False` | Make text bold |
| `background` | `str` | `None` | Background color |
| `border` | `bool` | `False` | Add border around message |
| `header` | `bool` | `False` | Format as header |
| `underline` | `bool` | `False` | Underline text |
| `urgent` | `bool` | `False` | Mark as urgent (affects formatting) |
| `emoji` | `bool` | `True` | Include emoji icons |

**Example:**
```python
logger.log_types("INFO", "Application started", emoji=True, bold=True)
logger.log_types("ERROR", "Database error", urgent=True, border=True)
logger.log_types("SUCCESS", "Operation completed", header=True)
```

### log_with_context()

Log messages with additional context and metadata.

```python
def log_with_context(self, 
                     level: str, 
                     message: str, 
                     context: dict = None, 
                     tags: list = None, 
                     **kwargs) -> None:
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `level` | `str` | Required | Log level |
| `message` | `str` | Required | Log message |
| `context` | `dict` | `None` | Additional context data |
| `tags` | `list` | `None` | Tags for categorization |
| `**kwargs` | | | Additional formatting options |

**Example:**
```python
logger.log_with_context(
    "INFO", 
    "User login",
    context={"user_id": 123, "ip": "192.168.1.1"},
    tags=["authentication", "security"]
)
```

### batch_log()

Process multiple log entries efficiently.

```python
def batch_log(self, log_entries: list) -> None:
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `log_entries` | `list` | List of log entries (tuples or dicts) |

**Example:**
```python
batch_logs = [
    ("INFO", "Starting batch process"),
    {"level": "DEBUG", "message": "Processing item 1"},
    ("SUCCESS", "Batch completed")
]
logger.batch_log(batch_logs)
```

## ⚡ Performance Monitoring

### log_function_time() (Decorator)

Decorator for automatic function timing.

```python
@logger.log_function_time
def my_function():
    # Function code here
    pass
```

**Features:**
- Automatic execution time measurement
- Memory usage tracking
- Error handling and logging
- Performance statistics collection

### performance_profile() (Context Manager)

Context manager for performance profiling.

```python
def performance_profile(self, operation_name: str):
```

**Example:**
```python
with logger.performance_profile("data_processing"):
    # Code to profile
    process_data()
```

### start_timer() / stop_timer()

Manual timing methods.

```python
def start_timer(self, timer_name: str) -> None:
def stop_timer(self, timer_name: str) -> float:
```

**Example:**
```python
logger.start_timer("database_query")
# Execute database query
execution_time = logger.stop_timer("database_query")
```

## 📊 System Monitoring

### add_custom_metric()

Add custom application metrics.

```python
def add_custom_metric(self, metric_name: str, value: float, timestamp: float = None) -> None:
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `metric_name` | `str` | Required | Name of the metric |
| `value` | `float` | Required | Metric value |
| `timestamp` | `float` | `None` | Custom timestamp (uses current time if None) |

**Example:**
```python
logger.add_custom_metric("response_time", 145.2)
logger.add_custom_metric("active_users", 50)
logger.add_custom_metric("memory_usage", 512.5)
```

### track_api_call()

Monitor API call performance.

```python
def track_api_call(self, 
                   endpoint: str, 
                   method: str, 
                   response_time: float, 
                   status_code: int) -> None:
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `endpoint` | `str` | API endpoint path |
| `method` | `str` | HTTP method (GET, POST, etc.) |
| `response_time` | `float` | Response time in milliseconds |
| `status_code` | `int` | HTTP status code |

**Example:**
```python
logger.track_api_call("/api/users", "GET", 125.5, 200)
logger.track_api_call("/api/login", "POST", 250.0, 401)
```

## 🔒 Security Logging

### log_security_event()

Log security-related events.

```python
def log_security_event(self, 
                       event_type: str, 
                       severity: str, 
                       description: str, 
                       additional_data: dict = None) -> None:
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `event_type` | `str` | Required | Type of security event |
| `severity` | `str` | Required | Severity level: LOW, MEDIUM, HIGH, CRITICAL |
| `description` | `str` | Required | Event description |
| `additional_data` | `dict` | `None` | Additional security context |

**Example:**
```python
logger.log_security_event(
    "LOGIN_ATTEMPT", 
    "MEDIUM", 
    "Failed login attempt from unknown IP",
    {"ip": "192.168.1.100", "attempts": 3}
)
```

## 📈 Analytics & Insights

### view_insights()

Generate and display comprehensive insights.

```python
def view_insights(self, 
                  detailed: bool = True, 
                  export_format: str = None, 
                  create_dashboard: bool = False) -> dict:
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `detailed` | `bool` | `True` | Include detailed analysis |
| `export_format` | `str` | `None` | Export format: "json", "csv" |
| `create_dashboard` | `bool` | `False` | Generate HTML dashboard |

**Returns:** Dictionary containing insights data

**Example:**
```python
insights = logger.view_insights(detailed=True, create_dashboard=True)
print(f"Health Score: {insights['health_score']}")
```

### generate_advanced_report()

Generate comprehensive analytics report.

```python
def generate_advanced_report(self) -> dict:
```

**Returns:** Dictionary containing:
- Executive summary
- Performance analysis
- Error statistics
- Recommendations
- System health metrics

**Example:**
```python
report = logger.generate_advanced_report()
print(f"Total Runtime: {report['executive_summary']['total_runtime']}")
print(f"Error Rate: {report['performance_analysis']['error_rate']}%")
```

### get_function_statistics()

Get detailed function performance statistics.

```python
def get_function_statistics(self) -> dict:
```

**Returns:** Dictionary with function performance data

**Example:**
```python
stats = logger.get_function_statistics()
for func_name, data in stats.items():
    print(f"{func_name}: {data['avg_time']}ms average")
```

## 🎨 Visualization

### draw_and_save_graph()

Generate performance graphs and charts.

```python
def draw_and_save_graph(self, graph_type: str = "all") -> str:
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `graph_type` | `str` | `"all"` | Graph type: "all", "performance", "errors", "system", "functions" |

**Returns:** Path to saved graph file

**Example:**
```python
graph_path = logger.draw_and_save_graph("performance")
print(f"Graph saved to: {graph_path}")
```

### create_html_dashboard()

Create interactive HTML dashboard.

```python
def create_html_dashboard(self) -> str:
```

**Returns:** Path to HTML dashboard file

**Example:**
```python
dashboard_path = logger.create_html_dashboard()
print(f"Dashboard created: {dashboard_path}")
```

## 💾 Database Operations

### query_logs()

Query stored log data.

```python
def query_logs(self, 
               start_time: str = None, 
               end_time: str = None, 
               level: str = None, 
               limit: int = 100) -> list:
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `start_time` | `str` | `None` | Start time filter (ISO format) |
| `end_time` | `str` | `None` | End time filter (ISO format) |
| `level` | `str` | `None` | Log level filter |
| `limit` | `int` | `100` | Maximum number of results |

**Returns:** List of log entries

**Example:**
```python
recent_errors = logger.query_logs(
    level="ERROR",
    start_time="2025-08-17T00:00:00",
    limit=50
)
```

## 📤 Export & Import

### export_data()

Export logging data in various formats.

```python
def export_data(self, 
                format_type: str = "json", 
                include_raw_data: bool = False, 
                filename: str = None) -> str:
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `format_type` | `str` | `"json"` | Export format: "json", "csv", "xml" |
| `include_raw_data` | `bool` | `False` | Include raw log data |
| `filename` | `str` | `None` | Custom filename |

**Returns:** Exported data as string or filename

**Example:**
```python
json_data = logger.export_data("json", include_raw_data=True)
csv_file = logger.export_data("csv", filename="session_data.csv")
```

## 🔧 Configuration & Management

### update_config()

Update logger configuration.

```python
def update_config(self, **kwargs) -> None:
```

**Example:**
```python
logger.update_config(
    log_level=logging.INFO,
    enable_alerts=True,
    alert_email="admin@example.com"
)
```

### start_monitoring() / stop_monitoring()

Control system monitoring.

```python
def start_monitoring(self) -> None:
def stop_monitoring(self) -> None:
```

**Example:**
```python
logger.start_monitoring()
# ... application code ...
logger.stop_monitoring()
```

## 🔌 Plugin System

### load_plugin()

Load external plugins.

```python
def load_plugin(self, plugin_name: str, plugin_config: dict = None) -> bool:
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `plugin_name` | `str` | Required | Plugin name |
| `plugin_config` | `dict` | `None` | Plugin configuration |

**Example:**
```python
success = logger.load_plugin("elasticsearch_exporter", {
    "host": "localhost",
    "port": 9200
})
```

## 🚨 Alert System

### set_alert_threshold()

Configure alert thresholds.

```python
def set_alert_threshold(self, metric: str, threshold: float, condition: str = "greater") -> None:
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `metric` | `str` | Required | Metric name |
| `threshold` | `float` | Required | Threshold value |
| `condition` | `str` | `"greater"` | Condition: "greater", "less", "equal" |

**Example:**
```python
logger.set_alert_threshold("cpu_usage", 80.0, "greater")
logger.set_alert_threshold("error_rate", 5.0, "greater")
```

## 🔄 Context Managers

### Context Manager Support

InsightLogger supports context managers for automatic cleanup:

```python
with InsightLogger("MyApp") as logger:
    logger.log_types("INFO", "Inside context")
    # Automatic cleanup when exiting context
```

### Performance Profiling Context

```python
with logger.performance_profile("operation_name") as profiler:
    # Code to profile
    expensive_operation()
# Automatic timing and reporting
```

## 📊 Data Structures

### Log Entry Format

```python
{
    "timestamp": "2025-08-17T10:30:45.123456",
    "level": "INFO",
    "message": "Log message",
    "context": {"key": "value"},
    "tags": ["tag1", "tag2"],
    "session_id": "abc123",
    "function_name": "my_function",
    "execution_time": 0.123,
    "memory_usage": 45.2
}
```

### Performance Metrics Format

```python
{
    "function_name": "my_function",
    "execution_times": [0.123, 0.145, 0.098],
    "avg_time": 0.122,
    "min_time": 0.098,
    "max_time": 0.145,
    "call_count": 3,
    "total_time": 0.366,
    "memory_usage": [45.2, 46.1, 44.8],
    "errors": 0
}
```

### System Metrics Format

```python
{
    "timestamp": 1692268245.123,
    "cpu_usage": 75.2,
    "memory_usage": 68.5,
    "disk_usage": 45.0,
    "network_io": {"bytes_sent": 1024, "bytes_recv": 2048},
    "process_count": 156,
    "uptime": 3600.5
}
```

## 🚀 Advanced Usage Examples

### Complete Application Example

```python
from insightlog import InsightLogger
import time

# Initialize with full configuration
logger = InsightLogger(
    name="ProductionApp",
    enable_database=True,
    enable_monitoring=True,
    enable_alerts=True,
    alert_email="admin@company.com",
    smtp_server="smtp.company.com",
    smtp_user="alerts@company.com",
    smtp_password="password"
)

# Configure alerts
logger.set_alert_threshold("cpu_usage", 80.0)
logger.set_alert_threshold("memory_usage", 85.0)
logger.set_alert_threshold("error_rate", 5.0)

# Application startup
logger.log_types("INFO", "🚀 Application starting", header=True)

@logger.log_function_time
def initialize_application():
    """Initialize application components"""
    logger.log_types("INFO", "Loading configuration")
    time.sleep(0.5)
    
    logger.log_types("INFO", "Connecting to database")
    time.sleep(1.0)
    
    logger.log_types("SUCCESS", "Application initialized")

# Main application logic
def main():
    try:
        initialize_application()
        
        # Simulate application work
        for i in range(10):
            with logger.performance_profile(f"task_{i}"):
                # Simulate work
                time.sleep(0.1)
                
                # Add metrics
                logger.add_custom_metric("tasks_completed", i + 1)
                logger.add_custom_metric("response_time", 100 + i * 5)
                
                # Log with context
                logger.log_with_context(
                    "INFO",
                    f"Completed task {i + 1}",
                    context={"task_id": i + 1, "duration": 0.1},
                    tags=["task", "processing"]
                )
        
        # Generate final report
        logger.log_types("INFO", "Generating final report")
        report = logger.generate_advanced_report()
        
        logger.log_types("SUCCESS", 
                        f"Application completed successfully! "
                        f"Health Score: {report['executive_summary']['health_score']:.1f}/100",
                        header=True)
        
        # Create dashboard
        dashboard = logger.create_html_dashboard()
        logger.log_types("INFO", f"Dashboard created: {dashboard}")
        
        # Export data
        export_file = logger.export_data("json", include_raw_data=True)
        logger.log_types("INFO", f"Data exported: {export_file}")
        
    except Exception as e:
        logger.log_types("CRITICAL", f"Application error: {str(e)}", urgent=True)
        logger.log_security_event("APPLICATION_ERROR", "HIGH", str(e))
        
    finally:
        logger.stop_monitoring()
        logger.log_types("INFO", "Application shutdown complete")

if __name__ == "__main__":
    main()
```

## 🎯 Best Practices

### 1. **Initialization**
```python
# Always use descriptive names
logger = InsightLogger("MyApplication")

# Enable features you need
logger = InsightLogger(
    name="WebService",
    enable_database=True,      # For log persistence
    enable_monitoring=True,    # For system metrics
    enable_alerts=False        # Only if email is configured
)
```

### 2. **Logging Levels**
```python
# Use appropriate log levels
logger.log_types("DEBUG", "Detailed debugging information")
logger.log_types("INFO", "General application flow")
logger.log_types("WARNING", "Potential issues")
logger.log_types("ERROR", "Error conditions")
logger.log_types("CRITICAL", "Critical failures")
```

### 3. **Performance Monitoring**
```python
# Use decorators for functions
@logger.log_function_time
def important_function():
    pass

# Use context managers for code blocks
with logger.performance_profile("database_operation"):
    execute_complex_query()
```

### 4. **Context and Metadata**
```python
# Always include relevant context
logger.log_with_context(
    "INFO",
    "User action",
    context={"user_id": 123, "action": "login", "ip": "192.168.1.1"},
    tags=["authentication", "security"]
)
```

### 5. **Error Handling**
```python
try:
    risky_operation()
except Exception as e:
    logger.log_types("ERROR", f"Operation failed: {str(e)}")
    logger.log_security_event("OPERATION_FAILURE", "MEDIUM", str(e))
```

---

## 📚 Related Documentation

- [Installation Guide](installation.md)
- [Quick Start Tutorial](quickstart.md)
- [Configuration Options](configuration.md)
- [Best Practices](best-practices.md)
- [Troubleshooting Guide](troubleshooting.md)

---

**This API reference covers all public methods and parameters.** For the most up-to-date information, always refer to the source code and inline documentation.

**Need Help?**
- 📧 Email: help@velyzo.de
- 🐛 Issues: [GitHub Issues](https://github.com/Velyzo/InsightLog/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/Velyzo/InsightLog/discussions)
