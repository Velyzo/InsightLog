<div align="center">
  
# InsightLog

[![License](https://img.shields.io/badge/License-MIT-blue)](https://github.com/Eldritchy/InsightLog#license)  [![PyPi](https://img.shields.io/badge/PyPi%20Link-FFFF00)](https://pypi.org/project/insightlog/)  <a href="https://github.com/D-I-Projects/diec/blob/master/CONTRIBUTING.md"> <img src="https://img.shields.io/github/contributors-anon/Eldritchy/InsightLog" alt="Contributors badge" /></a>  [![Downloads](https://static.pepy.tech/badge/insightlog)](https://pepy.tech/project/insightlog)

```bash
pip install insightlog
``` 

A powerful logging utility for better logging, visualizations, and more.

</div>

## Overview

`InsightLog` is a powerful logging utility designed to enhance the development experience by providing rich logging features, custom formats, and data visualization capabilities.

## Features

- **Custom Log Levels**: Define log messages with specialized methods like `success`, `alert`, or `highlight`.
- **File Rotation**: Automatically manage log file sizes and backups using `RotatingFileHandler`.
- **Data Visualizations**: Generate ASCII-based bar charts, pie charts, and more.
- **Styled Logging**: Add colors, highlights, and borders to your logs for better readability.
- **Dynamic Progress Bars**: Smoothly integrated progress tracking using `tqdm`.

---

## Installation

Install `InsightLog` with pip:

```bash
pip install insightlog
```

---

## Usage

### Setting Up a Logger

```python
import insightlog

# Create an instance of InsightLogger
log_instance = insightlog.setup(name="MyApp")

# Logging examples
log_instance.success("This is a success log.")
log_instance.failure("This is a failure log.")
log_instance.alert("This is an alert log.")
log_instance.trace("This is a trace log.")
log_instance.highlight("This is a highlighted log.")
log_instance.bordered("This is a bordered log.")
log_instance.header("This is a header log.")
log_instance.debug_underline("This is a debug underline log.")
log_instance.alert_urgent("This is an urgent alert log.")

# Visualizations
log_instance.draw_bar_chart()
log_instance.draw_pie_chart()
log_instance.draw_line_chart()
log_instance.draw_scatter_plot()
log_instance.draw_waterfall_chart()

# Progress bar
log_instance.draw_progress_bar(total=100, duration=5, description="Loading...")

# Table
data = [["Name", "Age", "Location"], ["John", 30, "New York"], ["Jane", 25, "Los Angeles"]]
log_instance.print_table(data)
log_instance.print_ascii_art("Sample ASCII Art")
log_instance.color_gradient("Gradient Text", start_color="red", end_color="blue")
log_instance.spin_animation(duration=5)
```

---

## Requirements

- Python >= 3.9
- `termcolor`
- `tqdm`

## License

MIT License. See [LICENSE](LICENSE) for details.

---

Author: **Eldritchy**  
Email: [eldritchy.help@gmail.com](mailto:eldritchy.help@gmail.com)  
GitHub: [https://github.com/Eldritchy](https://github.com/Eldritchy)