# Quick Start Tutorial

Welcome to InsightLogger! This tutorial will get you up and running in just a few minutes.

## 🚀 Your First InsightLogger Application

### Step 1: Basic Setup

Create a new Python file called `my_first_app.py`:

```python
from insightlog import InsightLogger

# Initialize the logger
logger = InsightLogger(
    name="MyFirstApp",
    enable_database=True,
    enable_monitoring=True
)

# Your first log message
logger.log_types("INFO", "Hello, InsightLogger!", emoji=True, bold=True)
```

Run it:
```bash
python my_first_app.py
```

You should see:
```
2025-08-17 10:30:45 - INFO - 📝 Hello, InsightLogger!
```

### Step 2: Add Performance Monitoring

Let's monitor a function's performance:

```python
from insightlog import InsightLogger
import time

logger = InsightLogger("PerformanceDemo")

@logger.log_function_time
def slow_function():
    """A function that takes some time"""
    time.sleep(2)
    return "Work completed!"

# Call the monitored function
result = slow_function()
logger.log_types("SUCCESS", f"Result: {result}")
```

Output:
```
⏱️ slow_function - Starting execution...
⏱️ slow_function - Completed in 2.01 seconds
✅ SUCCESS - Result: Work completed!
```

### Step 3: System Monitoring

Monitor your system resources:

```python
from insightlog import InsightLogger
import time

logger = InsightLogger(
    name="SystemMonitor",
    enable_monitoring=True
)

# Let monitoring collect data
logger.log_types("INFO", "Starting system monitoring...")
time.sleep(5)  # Let it collect some data

# View the insights
logger.view_insights()
```

### Step 4: Custom Metrics

Track application-specific metrics:

```python
from insightlog import InsightLogger
import random

logger = InsightLogger("MetricsDemo")

# Simulate application metrics
for i in range(10):
    response_time = random.uniform(100, 500)
    user_count = random.randint(50, 200)
    
    logger.add_custom_metric("response_time", response_time)
    logger.add_custom_metric("active_users", user_count)
    
    logger.log_types("DEBUG", f"Processed request {i+1}")

# View metrics summary
logger.view_insights(detailed=True)
```

## 🎯 Complete Example Application

Here's a complete example that demonstrates multiple features:

```python
from insightlog import InsightLogger
import time
import random

def main():
    # Initialize with full features
    logger = InsightLogger(
        name="CompleteDemo",
        enable_database=True,
        enable_monitoring=True,
        enable_alerts=False  # Set to True with email config for alerts
    )
    
    logger.log_types("INFO", "🚀 Starting Complete Demo Application", header=True)
    
    # Simulate application startup
    simulate_startup(logger)
    
    # Main application loop
    simulate_application_work(logger)
    
    # Handle some errors
    simulate_error_scenarios(logger)
    
    # Generate final report
    generate_report(logger)
    
    # Cleanup
    logger.stop_monitoring()
    logger.log_types("SUCCESS", "Demo completed successfully!", border=True)

def simulate_startup(logger):
    """Simulate application startup sequence"""
    startup_tasks = [
        ("Database connection", 1.2),
        ("Loading configuration", 0.5),
        ("Initializing modules", 0.8),
        ("Starting services", 1.0)
    ]
    
    for task, duration in startup_tasks:
        logger.log_types("INFO", f"Starting: {task}")
        time.sleep(duration)
        logger.log_types("SUCCESS", f"Completed: {task}")

@logger.log_function_time  # Note: This would need to be defined after logger creation
def simulate_application_work(logger):
    """Simulate main application work"""
    logger.log_types("INFO", "🔄 Starting main application work")
    
    for i in range(5):
        # Simulate processing
        process_time = random.uniform(0.5, 2.0)
        time.sleep(process_time)
        
        # Log with context
        logger.log_with_context(
            "INFO",
            f"Processed task {i+1}",
            context={
                "task_id": i+1,
                "duration": process_time,
                "status": "completed"
            },
            tags=["processing", "task", "work"]
        )
        
        # Add custom metrics
        logger.add_custom_metric("processing_time", process_time * 1000)
        logger.add_custom_metric("tasks_completed", i + 1)

def simulate_error_scenarios(logger):
    """Simulate various error scenarios"""
    logger.log_types("WARNING", "⚠️ Testing error handling")
    
    # Simulate different types of errors
    error_scenarios = [
        ("Network timeout", "WARNING"),
        ("Invalid input data", "ERROR"),
        ("Rate limit exceeded", "WARNING"),
        ("Critical system error", "CRITICAL")
    ]
    
    for error_msg, level in error_scenarios:
        logger.log_types(level, f"Simulated error: {error_msg}")
        
        # Log security event for critical errors
        if level == "CRITICAL":
            logger.log_security_event(
                "SYSTEM_ERROR",
                "HIGH",
                f"Critical error occurred: {error_msg}"
            )

def generate_report(logger):
    """Generate and display final report"""
    logger.log_types("INFO", "📊 Generating final report")
    
    # Create visualizations
    logger.draw_and_save_graph("all")
    
    # Export data
    json_data = logger.export_data("json")
    csv_data = logger.export_data("csv")
    
    # Generate advanced report
    report = logger.generate_advanced_report()
    
    logger.log_types("SUCCESS", "📋 Report generated successfully")
    print(f"Health Score: {report['executive_summary']['health_score']:.1f}/100")
    print(f"Total Runtime: {report['executive_summary']['total_runtime']}")

if __name__ == "__main__":
    main()
```

## 🎨 Customizing Your Logger

### Log Formatting Options

```python
from insightlog import InsightLogger

logger = InsightLogger("FormattingDemo")

# Different formatting options
logger.log_types("INFO", "Standard info message")
logger.log_types("SUCCESS", "Success with emoji", emoji=True)
logger.log_types("WARNING", "Bold warning", bold=True)
logger.log_types("ERROR", "Urgent error", urgent=True)
logger.log_types("INFO", "Message with border", border=True)
logger.log_types("SUCCESS", "Header message", header=True)
```

### Configuration Options

```python
logger = InsightLogger(
    name="ConfigDemo",
    save_log="enabled",           # Enable file logging
    log_dir="./logs",            # Custom log directory
    log_filename="app.log",      # Custom log filename
    max_bytes=5000000,           # 5MB max log file size
    backup_count=3,              # Keep 3 backup files
    log_level=logging.INFO,      # Set minimum log level
    enable_database=True,        # Enable SQLite database
    enable_monitoring=True,      # Enable system monitoring
    enable_alerts=False,         # Disable email alerts
)
```

### Using Context Managers

```python
from insightlog import InsightLogger

# Automatic cleanup with context manager
with InsightLogger("ContextDemo") as logger:
    logger.log_types("INFO", "Inside context manager")
    
    # Use performance profiling
    with logger.performance_profile("data_processing"):
        # Your code here
        time.sleep(1)
    
    logger.log_types("SUCCESS", "Context processing completed")

# Logger automatically cleaned up here
```

## 🔧 Integration Examples

### Web Framework Integration

#### Flask Example
```python
from flask import Flask
from insightlog import InsightLogger

app = Flask(__name__)
logger = InsightLogger("FlaskApp", enable_monitoring=True)

@app.route('/')
@logger.log_function_time
def home():
    logger.log_types("INFO", "Home page accessed")
    return "Hello World!"

@app.route('/api/data')
def api_data():
    logger.track_api_call("/api/data", "GET", 150, 200)
    return {"data": "example"}

if __name__ == "__main__":
    logger.log_types("INFO", "Starting Flask application")
    app.run(debug=True)
```

#### Django Example
```python
# In your Django views.py
from django.http import JsonResponse
from insightlog import InsightLogger

logger = InsightLogger("DjangoApp")

def my_view(request):
    logger.log_with_context(
        "INFO",
        "API request received",
        context={
            "method": request.method,
            "path": request.path,
            "user": str(request.user)
        }
    )
    
    # Your view logic here
    return JsonResponse({"status": "success"})
```

## 📊 Monitoring Dashboard

Create a real-time dashboard:

```python
from insightlog import InsightLogger
import time

logger = InsightLogger(
    name="DashboardDemo",
    enable_monitoring=True
)

# Run for a while to collect data
for i in range(30):
    logger.log_types("INFO", f"Processing item {i+1}")
    logger.add_custom_metric("items_processed", i + 1)
    time.sleep(1)

# Create dashboard
logger.view_insights(detailed=True, create_dashboard=True)
print("Dashboard created! Check the .insight directory for HTML files.")
```

## 🎯 Next Steps

Now that you've completed the quick start tutorial:

1. **[Explore Basic Examples](basic-examples.md)** - More code examples
2. **[Learn About Features](logging-features.md)** - Detailed feature documentation
3. **[Try the Demo App](tkinter-demo.md)** - Interactive demo application
4. **[Read Best Practices](best-practices.md)** - Recommended patterns
5. **[API Reference](api-reference.md)** - Complete API documentation

## 💡 Tips for Success

1. **Start Simple**: Begin with basic logging and gradually add features
2. **Monitor Early**: Enable monitoring from the beginning to catch issues
3. **Use Context**: Add context and tags to make logs more searchable
4. **Regular Reports**: Generate regular reports to track application health
5. **Dashboard Review**: Check the HTML dashboards for visual insights

## 🆘 Getting Help

If you run into issues:

- Check the [Troubleshooting Guide](installation.md#troubleshooting)
- Review the [API Documentation](api-reference.md)
- Open an issue on [GitHub](https://github.com/Velyzo/InsightLog/issues)
- Contact us at help@velyzo.de

---

**Congratulations!** 🎉 You've successfully completed the InsightLogger quick start tutorial. You're now ready to build amazing applications with comprehensive logging and monitoring!
