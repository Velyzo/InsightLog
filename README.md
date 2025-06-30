# **InsightLogger v1.4** 🔍

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.4.0-orange.svg)](https://github.com/Velyzo/InsightLog)

**InsightLogger** is a powerful, enterprise-grade logging and monitoring library for Python applications. It provides comprehensive insights into your application's performance, system health, and behavior with real-time monitoring, advanced analytics, and beautiful visualizations.

## **🌟 What's New in v1.4**

- 🎯 **Real-time System Monitoring**: CPU, memory, and network usage tracking
- 🔐 **Security Event Logging**: Built-in security monitoring and event tracking
- 📊 **Interactive HTML Dashboards**: Real-time web-based monitoring interface
- 🗄️ **Database Logging**: SQLite integration for persistent log storage
- 📧 **Smart Alerting**: Email notifications for critical events and thresholds
- 🔍 **Anomaly Detection**: Automatic detection of performance and behavior anomalies
- 📈 **Advanced Analytics**: Comprehensive performance profiling and bottleneck identification
- 🎨 **Enhanced Visualizations**: Multi-type charts, graphs, and performance reports
- 🔧 **Plugin System**: Extensible architecture for custom functionality
- 📤 **Data Export**: Multiple export formats (JSON, CSV) with comprehensive reports
- 🎪 **Context Managers**: Easy-to-use context managers for performance profiling
- 🏥 **Health Scoring**: Automatic calculation of system health scores
- 💾 **Log Compression**: Automatic compression of old log files
- 🔄 **Batch Logging**: Efficient processing of multiple log entries

---

## **✨ Key Features**

### **Advanced Logging**
- 🏷️ **Multiple Log Levels**: INFO, DEBUG, ERROR, SUCCESS, FAILURE, WARNING, ALERT, TRACE, HIGHLIGHT, CRITICAL
- 🎨 **Rich Formatting**: Colors, emojis, borders, highlighting, and custom styling
- 📝 **Context Logging**: Add metadata, tags, and contextual information
- 📦 **Batch Processing**: Efficiently process multiple log entries

### **Performance Monitoring**
- ⚡ **Function Timing**: Automatic execution time tracking with decorators
- 🔄 **Real-time Spinners**: Live progress indicators during function execution
- 💾 **Memory Tracking**: Monitor memory usage and memory deltas
- 📊 **Performance Profiling**: Detailed performance analysis and bottleneck identification

### **System Monitoring**
- 💻 **Resource Monitoring**: Real-time CPU and memory usage tracking
- 🌐 **Network Monitoring**: Network I/O statistics and monitoring
- 📈 **Custom Metrics**: Track application-specific metrics and KPIs
- 🔍 **API Monitoring**: Track API call performance and response times

### **Analytics & Insights**
- 🤖 **Anomaly Detection**: Automatic detection of unusual patterns and behaviors
- 💡 **Smart Recommendations**: AI-powered optimization suggestions
- 🏥 **Health Scoring**: Overall system health assessment (0-100 scale)
- 📋 **Comprehensive Reports**: Detailed performance and analysis reports

### **Security Features**
- 🔒 **Security Event Logging**: Track security-related events and incidents
- 🛡️ **Data Masking**: Automatic masking of sensitive information in logs
- 🚨 **Threat Detection**: Monitor for security threats and suspicious activities

### **Visualization & Reporting**
- 📊 **Advanced Charts**: Bar charts, time series, pie charts, and performance graphs
- 🌐 **HTML Dashboards**: Interactive web-based monitoring interface
- 📤 **Export Capabilities**: JSON, CSV, and custom format exports
- 📈 **Real-time Updates**: Live updating charts and metrics

### **Integration & Extensibility**
- 🗄️ **Database Integration**: SQLite for persistent logging and analysis
- 📧 **Email Alerts**: SMTP integration for critical event notifications
- 🔌 **Plugin System**: Extensible architecture for custom functionality
- 🎪 **Context Manager Support**: Easy integration with existing code

---

## **🚀 Installation**

The installation process remains **unchanged** to maintain compatibility:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Velyzo/InsightLogger.git
   cd InsightLogger
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the package:**
   ```bash
   pip install -e .
   ```

### **Dependencies**
- `termcolor>=2.0.0` - Enhanced terminal colors and formatting
- `matplotlib>=3.5.0` - Advanced plotting and visualization
- `tabulate>=0.9.0` - Beautiful table formatting
- `psutil>=5.8.0` - System and process monitoring
- `numpy>=1.21.0` - Numerical computing for analytics
- `tqdm>=4.64.0` - Progress bars and indicators

---

## **📖 Quick Start Guide**

### **Basic Usage**

```python
from insightlog import InsightLogger

# Initialize with enhanced features
logger = InsightLogger(
    name="MyApp",
    enable_database=True,
    enable_monitoring=True,
    enable_alerts=False
)

# Basic logging with enhanced formatting
logger.log_types("INFO", "Application started successfully", emoji=True, bold=True)
logger.log_types("SUCCESS", "Database connection established", border=True)
logger.log_types("WARNING", "Cache miss detected", background=True)
logger.log_types("ERROR", "Failed to connect to API", urgent=True)

# Function performance monitoring
@logger.log_function_time
def process_data():
    import time
    time.sleep(2)  # Simulate work
    return "Data processed"

result = process_data()

# View comprehensive insights
logger.view_insights(detailed=True, create_dashboard=True)
```

### **Advanced Usage with Context Manager**

```python
from insightlog import InsightLogger

# Use as context manager for automatic cleanup
with InsightLogger(
    name="AdvancedApp",
    enable_database=True,
    enable_monitoring=True,
    enable_alerts=True,
    alert_email="admin@company.com",
    smtp_server="smtp.gmail.com",
    smtp_user="alerts@company.com",
    smtp_password="your_password"
) as logger:
    
    # Performance profiling
    with logger.performance_profile("data_processing"):
        # Your code here
        data = [i**2 for i in range(100000)]
    
    # Custom metrics
    logger.add_custom_metric("user_count", 1500)
    logger.add_custom_metric("active_sessions", 45)
    
    # API monitoring
    logger.track_api_call("/api/users", "GET", response_time=234, status_code=200)
    
    # Security logging
    logger.log_security_event("LOGIN_ATTEMPT", "LOW", "User login from new device")
    
    # Contextual logging
    logger.log_with_context(
        "INFO",
        "User action performed",
        context={"user_id": 12345, "action": "file_upload"},
        tags=["user_activity", "audit"]
    )
    
    # Batch logging
    logs = [
        {"level": "INFO", "message": "Processing item 1"},
        {"level": "INFO", "message": "Processing item 2"},
        ("SUCCESS", "Batch processing completed")
    ]
    logger.batch_log(logs)

# Automatic cleanup and final report generated
```

---

## **🔧 Configuration Options**

### **Logger Initialization Parameters**

```python
logger = InsightLogger(
    name="MyLogger",                    # Logger name
    save_log="enabled",                 # Enable/disable file logging
    log_dir=".insight",                 # Log directory
    log_filename="app.log",             # Log filename
    max_bytes=1000000,                  # Max log file size
    backup_count=1,                     # Number of backup files
    log_level=logging.DEBUG,            # Logging level
    enable_database=True,               # Enable SQLite logging
    enable_monitoring=True,             # Enable system monitoring
    enable_alerts=False,                # Enable email alerts
    alert_email="admin@example.com",    # Alert email address
    smtp_server="smtp.gmail.com",       # SMTP server
    smtp_port=587,                      # SMTP port
    smtp_user="user@gmail.com",         # SMTP username
    smtp_password="password"            # SMTP password
)
```

### **Alert Thresholds**

```python
# Customize alert thresholds
logger.alert_thresholds = {
    'cpu_usage': 80,        # CPU usage percentage
    'memory_usage': 85,     # Memory usage percentage
    'error_rate': 10,       # Error rate percentage
    'response_time': 5000   # Response time in milliseconds
}
```

---

## **📊 Logging Levels & Formatting**

### **Available Log Levels**

| Level | Description | Color | Emoji |
|-------|-------------|-------|-------|
| `INFO` | General information | Cyan | ℹ️ |
| `SUCCESS` | Successful operations | Green | ✅ |
| `WARNING` | Warning messages | Yellow | ⚠️ |
| `ERROR` | Error messages | Red | 💥 |
| `CRITICAL` | Critical errors | Red | 🔥 |
| `DEBUG` | Debug information | Blue | 🐛 |
| `ALERT` | Alert notifications | Magenta | 🚨 |
| `TRACE` | Trace information | Cyan | 🔍 |
| `HIGHLIGHT` | Important highlights | Yellow | ⭐ |
| `FAILURE` | Failed operations | Red | ❌ |

### **Formatting Options**

```python
# Enhanced formatting options
logger.log_types("INFO", "Message", 
                 emoji=True,        # Add emoji icons
                 bold=True,         # Bold text
                 underline=True,    # Underlined text
                 border=True,       # Add borders
                 background=True,   # Background highlighting
                 urgent=True)       # Blinking text
```

---

## **🎯 Advanced Features**

### **Performance Profiling**

```python
# Method 1: Decorator
@logger.log_function_time
def expensive_function():
    # Your code here
    pass

# Method 2: Context Manager
with logger.performance_profile("operation_name"):
    # Your code here
    pass
```

### **Custom Metrics & Monitoring**

```python
# Add custom application metrics
logger.add_custom_metric("active_users", 150)
logger.add_custom_metric("cache_hit_rate", 0.95)
logger.add_custom_metric("database_connections", 25)

# Track API performance
logger.track_api_call("/api/data", "POST", response_time=345, status_code=201)

# Monitor system resources (automatic)
# CPU, memory, and network usage tracked in background
```

### **Security & Compliance**

```python
# Log security events
logger.log_security_event("FAILED_LOGIN", "MEDIUM", "Multiple failed attempts")
logger.log_security_event("PRIVILEGE_ESCALATION", "HIGH", "Unauthorized access")

# Secure logging with data masking
from insightlog import secure_log_decorator

@secure_log_decorator(logger, mask_patterns=[r'\d{4}-\d{4}-\d{4}-\d{4}'])
def process_payment(card_number):
    # Sensitive data automatically masked in logs
    pass
```

### **Database Integration**

```python
# Query log database
filtered_logs = logger.create_log_filter(
    level="ERROR",
    start_time=datetime.datetime(2024, 1, 1),
    end_time=datetime.datetime.now(),
    function_name="process_data"
)

# Get function statistics
stats = logger.get_function_statistics()
for func_name, metrics in stats.items():
    print(f"{func_name}: {metrics['avg_time']:.2f}ms average")
```

### **Anomaly Detection & Health Monitoring**

```python
# Detect system anomalies
anomalies = logger.detect_anomalies()
for anomaly in anomalies:
    print(f"⚠️ Anomaly detected: {anomaly}")

# Get system health score
health_score = logger._calculate_health_score()
print(f"System Health: {health_score}/100")

# Get optimization recommendations
recommendations = logger._generate_recommendations()
for rec in recommendations:
    print(f"💡 {rec['category']}: {rec['message']}")
```

---

## **📈 Visualization & Reports**

### **Generate Comprehensive Reports**

```python
# View detailed insights
logger.view_insights(
    detailed=True,              # Include detailed analysis
    export_format="json",       # Export data
    create_dashboard=True       # Generate HTML dashboard
)

# Generate advanced analytics report
report = logger.generate_advanced_report()
print(f"Health Score: {report['executive_summary']['health_score']}")
```

### **Export Data**

```python
# Export to JSON with raw data
json_file = logger.export_data("json", include_raw_data=True)

# Export to CSV for analysis
csv_file = logger.export_data("csv")

# Create interactive HTML dashboard
dashboard_path = logger.create_dashboard_html()
```

### **Chart Types Generated**

- 📊 **Log Frequency Bar Charts**: Distribution of log levels
- 📈 **System Resource Time Series**: CPU and memory usage over time  
- ⚡ **Function Performance Analysis**: Execution times and call distributions
- 🔍 **Performance Trends**: Function performance over time
- 🚨 **Error Rate Analysis**: Error rates by function
- 🌐 **Interactive Dashboards**: Real-time web interface

---

## **🔌 Integration Examples**

### **Flask Web Application**

```python
from flask import Flask
from insightlog import InsightLogger

app = Flask(__name__)
logger = InsightLogger("FlaskApp", enable_monitoring=True)

@app.route('/api/data')
@logger.log_function_time
def get_data():
    logger.track_api_call("/api/data", "GET", 
                         response_time=234, status_code=200)
    return {"data": "example"}

@app.errorhandler(500)
def handle_error(error):
    logger.log_types("ERROR", f"Server error: {error}")
    logger.log_security_event("SERVER_ERROR", "HIGH", str(error))
    return "Internal Server Error", 500
```

### **Data Processing Pipeline**

```python
from insightlog import InsightLogger, MetricsCollector

with InsightLogger("DataPipeline", enable_database=True) as logger:
    metrics = MetricsCollector(logger)
    
    # Track data processing stages
    with metrics.time_operation("data_extraction"):
        # Extract data
        metrics.count_event("records_extracted")
    
    with metrics.time_operation("data_transformation"):
        # Transform data
        metrics.gauge_value("data_quality_score", 0.95)
    
    with metrics.time_operation("data_loading"):
        # Load data
        metrics.count_event("records_loaded")
```

### **Microservice with Health Checks**

```python
from insightlog import InsightLogger
import requests

logger = InsightLogger("MicroService", 
                      enable_alerts=True,
                      alert_email="ops@company.com")

def health_check():
    """Comprehensive service health check"""
    try:
        # Check database
        with logger.performance_profile("db_health_check"):
            # Database check logic
            pass
        
        # Check external APIs
        response_time = logger.track_api_call("/health", "GET", 150, 200)
        
        # Calculate and log health metrics
        health_score = logger._calculate_health_score()
        logger.add_custom_metric("service_health", health_score)
        
        if health_score < 70:
            logger.log_types("ALERT", f"Service health degraded: {health_score}/100")
            
        return health_score > 80
        
    except Exception as e:
        logger.log_types("CRITICAL", f"Health check failed: {e}")
        logger.log_security_event("HEALTH_CHECK_FAILURE", "HIGH", str(e))
        return False
```

---

## **📁 Output Files & Structure**

InsightLogger creates a comprehensive set of output files in the `.insight` directory:

```
.insight/
├── app.log                           # Standard log file
├── insights_[session_id].db          # SQLite database
├── dashboard_[session_id].html       # Interactive dashboard
├── log_frequency_[timestamp].png     # Log level frequency chart
├── system_metrics_[timestamp].png    # System resource usage
├── function_performance_[timestamp].png # Function performance analysis
├── insight_export_[timestamp].json   # Exported data (JSON)
├── insight_export_[timestamp].csv    # Exported data (CSV)
└── plugins/                          # Custom plugins directory
```

---

## **🎛️ Configuration Best Practices**

### **Production Environment**

```python
# Production configuration
logger = InsightLogger(
    name="ProductionApp",
    log_level=logging.INFO,          # Reduce verbosity
    enable_database=True,            # Enable for analytics
    enable_monitoring=True,          # Monitor system health
    enable_alerts=True,              # Enable critical alerts
    alert_email="ops@company.com",   # Operations team
    max_bytes=10000000,              # 10MB log files
    backup_count=5                   # Keep 5 backups
)

# Set production alert thresholds
logger.alert_thresholds = {
    'cpu_usage': 85,
    'memory_usage': 90, 
    'error_rate': 5,
    'response_time': 3000
}
```

### **Development Environment**

```python
# Development configuration
logger = InsightLogger(
    name="DevApp",
    log_level=logging.DEBUG,         # Verbose logging
    enable_database=True,            # For analysis
    enable_monitoring=True,          # Performance insights
    enable_alerts=False,             # No email alerts
    create_dashboard=True            # Visual debugging
)
```

### **Testing Environment**

```python
# Testing configuration
logger = InsightLogger(
    name="TestApp",
    save_log="disabled",             # No file logging
    enable_database=False,           # No persistence needed
    enable_monitoring=False,         # No system monitoring
    enable_alerts=False              # No alerts during tests
)
```

---

## **🤝 Contributing**

We welcome contributions to InsightLogger! Here's how you can help:

### **Development Setup**

1. **Fork the repository**
2. **Create a virtual environment:**
   ```bash
   python -m venv insight_env
   source insight_env/bin/activate  # Linux/Mac
   # or
   insight_env\Scripts\activate     # Windows
   ```

3. **Install development dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Run tests:**
   ```bash
   python -m pytest tests/
   ```

### **Contributing Guidelines**

- 🐛 **Bug Reports**: Use GitHub issues with detailed reproduction steps
- ✨ **Feature Requests**: Propose new features with use cases
- 📝 **Documentation**: Improve docs and examples
- 🧪 **Testing**: Add tests for new features
- 🔧 **Code Quality**: Follow PEP 8 and include type hints

### **Development Areas**

- 🔌 **Plugin System**: Create custom plugins
- 📊 **Visualizations**: New chart types and dashboards
- 🔍 **Analytics**: Advanced anomaly detection algorithms
- 🔐 **Security**: Enhanced security monitoring features
- 🌐 **Integrations**: New framework and service integrations

---

## **📜 License**

InsightLogger is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## **🔗 Links & Resources**

- 📖 **Documentation**: [GitHub Wiki](https://github.com/Velyzo/InsightLog/wiki)
- 🐛 **Bug Tracker**: [GitHub Issues](https://github.com/Velyzo/InsightLog/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Velyzo/InsightLog/discussions)
- 📧 **Support**: [Email Support](mailto:help@velyzo.de)

---

## **👨‍💻 Author**

**InsightLogger v1.4** is developed and maintained by **Velyzo**.

- 🌐 **GitHub**: [@Velyzo](https://github.com/Velyzo)
- 📧 **Email**: Velyzo.help@web.de

---

## **🎉 Acknowledgments**

Special thanks to all contributors and the open-source community for making InsightLogger better with each release!

---

*InsightLogger v1.4 - Powering the next generation of Python application monitoring and analytics* 🚀
