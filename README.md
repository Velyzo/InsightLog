# **InsightLogger**

`InsightLogger` is an advanced, customizable logging library designed for Python applications. It helps developers track application performance, log detailed error messages, visualize data through charts, and create summaries of application execution.

## **Features**

- **Flexible Logging**: Supports multiple log levels (INFO, DEBUG, ERROR, etc.) with customizable formatting.
- **Rotating Logs**: Automatically manages log file size to prevent excessive disk usage.
- **Execution Time Tracking**: Decorate functions to measure and log execution time with live spinning animation.
- **Log Visualization**: Automatically generate bar graphs showing log level frequencies.
- **Environment Summary**: Generate detailed summaries of the runtime environment and execution statistics.
- **Enhanced Formatting**: Add styles like bold, underline, headers, and more to log messages.

---

## **Installation**

1. Clone the repository:

   ```bash
   git clone https://github.com/VelisCore/InsightLogger.git
   ```

2. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   Dependencies include:
   - `termcolor`
   - `matplotlib`
   - `tabulate`
   - `psutil`

---

## **Usage**

### **Getting Started**

```python
from insightlog import InsightLogger

# Initialize the logger
logger = InsightLogger(name="AppLog")

@logger.log_function_time
def example_function():
    time.sleep(2)

# Logging
logger.log_types("INFO", "This is an info log.")
logger.log_types("ERROR", "An error occurred.")

# Visualize logs and generate a summary
logger.draw_and_save_graph()
summary = logger.generate_log_summary()
logger.logger.info("\nSummary of Logs:\n" + summary)
```

### **Decorators**

Measure execution time for any function:

```python
@logger.log_function_time
def sample_function():
    time.sleep(1.5)
```

### **Log Levels**

Supported log levels include:
- `INFO`
- `ERROR`
- `SUCCESS`
- `FAILURE`
- `WARNING`
- `DEBUG`
- `ALERT`
- `TRACE`
- `HIGHLIGHT`
- `CRITICAL`

### **Environment Summary**

`InsightLogger` automatically collects environment information, such as:
- Python version
- Operating system and version
- Machine specifications (CPU, memory, etc.)
- Execution start and end times

---

## **Example Output**

### Console Output

```
[INFO] This is an info log.
[ERROR] An error occurred.
Function 'example_function' executed in 1500.12 ms.
```

### Summary Table

| Environment Info       | Details                 |
|------------------------|-------------------------|
| Python Version         | 3.10                   |
| Operating System       | Windows                |
| Memory                 | 16.00 GB               |
| Total Errors           | 1                      |

### Log Frequency Graph

![Log Frequency](.Insight/2023-12-01/log_frequency.png)

---

## **Contribution**

We welcome contributions to `InsightLogger`. To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with detailed descriptions of changes.

---

## **License**

`InsightLogger` is licensed under the MIT License. See `LICENSE` for details.

---

## **Support**

For issues or feature requests, please [open an issue](https://github.com/VelisCore/InsightLogger/issues).

---

## **Author**

Developed by **VelisCore**.
