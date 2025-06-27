# **InsightLogger**

`InsightLogger` is an advanced, customizable logging library designed for Python applications. It enables performance monitoring, detailed error logging, visual log representation, and execution summaries to gain better insights.

## **Features**

- **Flexible Logging**: Supports multiple log levels (INFO, DEBUG, ERROR, etc.) with customizable formats and handles both console and file logs.
- **Rotating Logs**: Automatically manages log file sizes and prevents excessive disk usage through rotating log files.
- **Execution Time Tracking**: Use decorators to measure and log the execution time of functions, including a live spinning animation during function execution.
- **Log Visualization**: Automatically generates bar charts that display the frequency of different log levels.
- **Environmental Insights**: Captures and displays detailed runtime environment information, including system specs and resource usage.
- **Advanced Log Formatting**: Adds visual styles like bold, underline, and headers to log messages for better clarity.

---

## **Installation**

1. Clone the repository:

    ```bash
    git clone https://github.com/Velyzo/InsightLogger.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

Dependencies include:

- `termcolor` for colored console output.
- `matplotlib` for visualizing logs.
- `tabulate` for neatly formatted tables.
- `psutil` for monitoring system resources.

## **Usage**

### Getting Started

```python
from insightlog import InsightLogger

# Initialize the logger
logger = InsightLogger(name="AppLog")

@logger.log_function_time
def example_function():
     time.sleep(2)

# Logging
logger.log("INFO", "This is an info log.")
logger.log("ERROR", "An error occurred.")

# Visualize logs and generate a summary
logger.generate_log_visualization()
summary = logger.generate_execution_summary()
logger.logger.info("\nLog Summary:\n" + summary)
```

### Logging Example

You can log messages with various severity levels such as INFO, ERROR, SUCCESS, WARNING, etc.

```python
logger.log("INFO", "This is an info message.")
logger.log("ERROR", "An error occurred.")
```

### Execution Time Tracking

Use the `@log_function_time` decorator to measure and log the execution time of functions.

```python
@logger.log_function_time
def sample_function():
     time.sleep(1.5)
```

### Log Levels

Supported log levels include:

- INFO
- ERROR
- SUCCESS
- FAILURE
- WARNING
- DEBUG
- ALERT
- TRACE
- CRITICAL

Each log level has its own format for console output.

### Insights and Visualization

After logging, InsightLogger provides valuable insights including:

- **Environmental Info**: Python version, OS version, machine specs (CPU, memory, etc.), and uptime.
- **Log Level Distribution**: A bar chart showing the frequency of each log level.

```python
logger.generate_environment_summary()  # Displays environment details
logger.generate_log_visualization()    # Generates and saves the log distribution chart
```

### Sample Output

Console Output:

```
[INFO] This is an info log.
[ERROR] An error occurred.
Function 'example_function' executed in 1500.12 ms.
```

Environment Summary:

| Environment Info | Details       |
|------------------|---------------|
| Python Version   | 3.10          |
| OS               | Windows       |
| RAM              | 16.00 GB      |
| Total Errors     | 1             |

Log Frequency Chart: (Bar chart displaying the frequency of different log levels)

## **Advanced Features**

- **Rotating Logs**: Configure log rotation to prevent excessive disk usage.
- **Real-Time Execution Tracker**: Display the real-time execution time of functions with a live spinning animation.
- **Error and Execution Tracking**: Track error counts, execution times, and resource usage (CPU, memory).

## **Contributing**

Contributions to InsightLogger are welcome. To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with detailed descriptions of the changes.

## **License**

InsightLogger is licensed under the MIT License. See LICENSE for details.

## **Support**

For issues or feature requests, please open an issue.

## **Author**

Developed by Velyzo.

## **Additional Notes**

- InsightLogger automatically creates a folder named `.insight` to store logs and visualizations.
- The logging system supports both console output and file logs, with rotation based on size.