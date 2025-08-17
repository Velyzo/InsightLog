# Troubleshooting Guide

Comprehensive troubleshooting guide for common issues with InsightLogger.

## 🔧 Common Issues and Solutions

### 1. Installation Issues

#### Python Version Compatibility

**Problem**: ImportError or module not found errors

```bash
ImportError: No module named 'insightlog'
```

**Solutions**:

```bash
# Check Python version (requires 3.9+)
python --version

# Install for specific Python version
python3.11 -m pip install insightlog

# Install in virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install insightlog
```

#### Dependency Conflicts

**Problem**: Package dependency conflicts

```bash
ERROR: pip's dependency resolver does not currently have a working solution
```

**Solutions**:

```bash
# Create fresh virtual environment
python -m venv fresh_env
fresh_env\Scripts\activate  # Windows
# or
source fresh_env/bin/activate  # Linux/Mac

# Install with specific versions
pip install insightlog==1.4.0

# Install without dependencies (advanced)
pip install insightlog --no-deps

# Then install dependencies manually
pip install matplotlib plotly psutil
```

#### Permission Issues

**Problem**: Permission denied during installation

**Solutions**:

```bash
# Install for current user only
pip install --user insightlog

# Use sudo (Linux/Mac only)
sudo pip install insightlog

# Use administrator command prompt (Windows)
# Right-click Command Prompt -> "Run as administrator"
pip install insightlog
```

### 2. File System Issues

#### Log Directory Permission Errors

**Problem**: 
```python
PermissionError: [Errno 13] Permission denied: './insight/app.log'
```

**Solution**:

```python
import os
from pathlib import Path
from insightlog import InsightLogger

# Use user home directory
user_home = Path.home()
log_dir = user_home / "app_logs"

# Create directory if it doesn't exist
log_dir.mkdir(exist_ok=True)

# Initialize logger with accessible directory
logger = InsightLogger(
    name="MyApp",
    log_dir=str(log_dir)
)
```

**Alternative Solutions**:

```python
# 1. Check and create directory with proper permissions
import os
import stat

def create_log_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
        # Set read/write permissions for owner
        os.chmod(path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        return True
    except PermissionError:
        print(f"Permission denied: {path}")
        return False

# 2. Use temporary directory
import tempfile

temp_dir = tempfile.mkdtemp()
logger = InsightLogger("MyApp", log_dir=temp_dir)

# 3. Disable file logging
logger = InsightLogger("MyApp", save_log="disabled")
```

#### Log File Rotation Issues

**Problem**: Log files not rotating properly

**Symptoms**:
- Single log file grows very large
- Backup files not created
- Disk space issues

**Solutions**:

```python
# 1. Check file permissions
import os

log_file = ".insight/app.log"
if os.path.exists(log_file):
    file_stat = os.stat(log_file)
    print(f"File size: {file_stat.st_size} bytes")
    print(f"File permissions: {oct(file_stat.st_mode)[-3:]}")

# 2. Manually configure rotation
logger = InsightLogger(
    name="MyApp",
    max_bytes=1000000,    # 1MB - smaller for testing
    backup_count=5,       # Keep 5 backups
    log_filename="test.log"
)

# 3. Test rotation
for i in range(1000):
    logger.log_types("INFO", f"Test message {i} - " + "x" * 100)
```

### 3. Database Issues

#### SQLite Database Lock

**Problem**:
```python
sqlite3.OperationalError: database is locked
```

**Solutions**:

```python
# 1. Ensure proper cleanup
from insightlog import InsightLogger

try:
    logger = InsightLogger("MyApp", enable_database=True)
    # ... use logger ...
finally:
    logger.close_database()  # Ensure connection is closed

# 2. Use context manager
from contextlib import contextmanager

@contextmanager
def get_logger():
    logger = InsightLogger("MyApp", enable_database=True)
    try:
        yield logger
    finally:
        logger.close_database()

# Usage
with get_logger() as logger:
    logger.log_types("INFO", "Test message")

# 3. Disable database for problematic environments
logger = InsightLogger("MyApp", enable_database=False)
```

#### Database Corruption

**Problem**: Database file is corrupted

**Solutions**:

```python
import os
import sqlite3
from insightlog import InsightLogger

def fix_database_corruption(db_path):
    try:
        # Test database integrity
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()
        conn.close()
        
        if result[0] != "ok":
            print("Database corruption detected")
            # Backup and recreate
            backup_path = db_path + ".backup"
            os.rename(db_path, backup_path)
            print(f"Corrupted database moved to {backup_path}")
            return True
    except Exception as e:
        print(f"Database check failed: {e}")
        return False

# Check and fix database
db_path = ".insight/insights_session.db"
if os.path.exists(db_path):
    fix_database_corruption(db_path)

# Create new logger (will create new database)
logger = InsightLogger("MyApp", enable_database=True)
```

#### Database Query Errors

**Problem**: Errors when querying logs

**Solutions**:

```python
# 1. Check database exists and has data
logger = InsightLogger("MyApp", enable_database=True)

try:
    # Test basic query
    logs = logger.query_logs(limit=1)
    print(f"Found {len(logs)} logs")
except Exception as e:
    print(f"Query error: {e}")
    
    # Recreate database
    logger.close_database()
    import os
    db_path = os.path.join(logger.log_dir, "insights_session.db")
    if os.path.exists(db_path):
        os.remove(db_path)
    logger._init_database()  # Recreate database

# 2. Add test data and verify
logger.log_types("INFO", "Test message")
logs = logger.query_logs(limit=1)
assert len(logs) > 0, "No logs found after insertion"
```

### 4. Monitoring Issues

#### High CPU Usage

**Problem**: InsightLogger causing high CPU usage

**Solutions**:

```python
# 1. Disable monitoring
logger = InsightLogger("MyApp", enable_monitoring=False)

# 2. Reduce monitoring frequency
logger = InsightLogger("MyApp", enable_monitoring=True)
# Adjust monitoring interval (if available)
if hasattr(logger, 'monitoring_interval'):
    logger.monitoring_interval = 10  # Every 10 seconds instead of 1

# 3. Monitor specific metrics only
logger = InsightLogger("MyApp", enable_monitoring=True)
# Disable expensive operations
logger.enable_system_metrics = False  # If available
```

#### Memory Leaks

**Problem**: Memory usage continuously increasing

**Solutions**:

```python
import gc
from insightlog import InsightLogger

# 1. Periodic cleanup
def periodic_cleanup(logger):
    logger.stop_monitoring()
    logger.close_database()
    gc.collect()  # Force garbage collection
    
    # Reinitialize if needed
    logger._init_database()
    logger.start_monitoring()

# 2. Use lightweight configuration
logger = InsightLogger(
    name="LightweightApp",
    enable_database=False,     # No database overhead
    enable_monitoring=False,   # No monitoring overhead
    max_bytes=1000000,        # Smaller log files
    backup_count=2            # Fewer backups
)

# 3. Monitor memory usage
import psutil
import threading
import time

def monitor_memory():
    process = psutil.Process()
    while True:
        memory_mb = process.memory_info().rss / 1024 / 1024
        print(f"Memory usage: {memory_mb:.1f} MB")
        if memory_mb > 500:  # Alert if over 500MB
            print("WARNING: High memory usage detected")
        time.sleep(60)

# Start memory monitoring
memory_thread = threading.Thread(target=monitor_memory, daemon=True)
memory_thread.start()
```

### 5. Email Alert Issues

#### SMTP Authentication Failures

**Problem**: 
```python
SMTPAuthenticationError: (535, '5.7.8 Username and Password not accepted')
```

**Solutions**:

```python
# 1. Gmail - Use App Passwords
logger = InsightLogger(
    name="MyApp",
    enable_alerts=True,
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    smtp_user="your_email@gmail.com",
    smtp_password="your_app_password"  # Not your regular password!
)

# 2. Test SMTP connection separately
import smtplib

def test_smtp_connection(server, port, user, password):
    try:
        smtp = smtplib.SMTP(server, port)
        smtp.starttls()
        smtp.login(user, password)
        smtp.quit()
        print("SMTP connection successful")
        return True
    except Exception as e:
        print(f"SMTP connection failed: {e}")
        return False

# Test before using with logger
test_smtp_connection("smtp.gmail.com", 587, "user@gmail.com", "app_password")

# 3. Alternative SMTP configurations
# Outlook/Hotmail
outlook_config = {
    "smtp_server": "smtp-mail.outlook.com",
    "smtp_port": 587,
    "smtp_user": "your_email@outlook.com",
    "smtp_password": "your_password"
}

# Corporate Exchange
exchange_config = {
    "smtp_server": "mail.company.com",
    "smtp_port": 25,  # or 587
    "smtp_user": "username",
    "smtp_password": "password"
}
```

#### Email Not Sent

**Problem**: No error but emails not received

**Solutions**:

```python
# 1. Check spam folder and enable debugging
import logging

# Enable SMTP debugging
logging.getLogger('smtplib').setLevel(logging.DEBUG)

logger = InsightLogger(
    name="MyApp",
    enable_alerts=True,
    alert_email="admin@company.com",
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    smtp_user="alerts@gmail.com",
    smtp_password="app_password"
)

# 2. Test with multiple recipients
logger = InsightLogger(
    name="MyApp",
    enable_alerts=True,
    alert_email="admin@company.com,backup@company.com",
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    smtp_user="alerts@gmail.com",
    smtp_password="app_password"
)

# 3. Manual email test
def test_email_sending():
    try:
        logger.log_types("CRITICAL", "Test alert message")
        print("Alert sent successfully")
    except Exception as e:
        print(f"Alert failed: {e}")

test_email_sending()
```

### 6. Import and Module Issues

#### Module Import Errors

**Problem**:
```python
ModuleNotFoundError: No module named 'insightlog'
```

**Solutions**:

```python
# 1. Check installation
import sys
print("Python path:", sys.path)

try:
    import insightlog
    print("InsightLogger installed successfully")
    print("Version:", insightlog.__version__ if hasattr(insightlog, '__version__') else "Unknown")
except ImportError as e:
    print(f"Import error: {e}")

# 2. Add path manually (temporary solution)
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'insightlog'))

from insightlog import InsightLogger

# 3. Reinstall package
# pip uninstall insightlog
# pip install insightlog
```

#### Circular Import Issues

**Problem**: Circular import errors in complex applications

**Solutions**:

```python
# 1. Delayed import
def get_logger():
    from insightlog import InsightLogger
    return InsightLogger("MyApp")

# 2. Module-level configuration
# config.py
class LoggerConfig:
    _logger = None
    
    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            from insightlog import InsightLogger
            cls._logger = InsightLogger("MyApp")
        return cls._logger

# Usage in other modules
from config import LoggerConfig
logger = LoggerConfig.get_logger()

# 3. Factory pattern
class LoggerFactory:
    @staticmethod
    def create_logger(name):
        from insightlog import InsightLogger
        return InsightLogger(name)
```

### 7. Performance Issues

#### Slow Logging Performance

**Problem**: Logging operations taking too long

**Solutions**:

```python
import time
from insightlog import InsightLogger

# 1. Measure logging performance
def measure_logging_performance():
    logger = InsightLogger("PerfTest", enable_database=False)
    
    start_time = time.time()
    for i in range(1000):
        logger.log_types("INFO", f"Test message {i}")
    end_time = time.time()
    
    print(f"1000 log messages took {end_time - start_time:.2f} seconds")

measure_logging_performance()

# 2. Optimize configuration for performance
fast_logger = InsightLogger(
    name="FastApp",
    enable_database=False,     # Disable database for speed
    enable_monitoring=False,   # Disable monitoring for speed
    save_log="disabled"        # Disable file logging for speed
)

# 3. Batch logging for high-volume applications
class BatchLogger:
    def __init__(self, batch_size=100):
        self.logger = InsightLogger("BatchApp")
        self.batch = []
        self.batch_size = batch_size
    
    def log(self, level, message):
        self.batch.append((level, message, time.time()))
        if len(self.batch) >= self.batch_size:
            self.flush()
    
    def flush(self):
        for level, message, timestamp in self.batch:
            self.logger.log_types(level, message)
        self.batch.clear()

batch_logger = BatchLogger()
```

#### Large Log File Issues

**Problem**: Log files becoming too large to manage

**Solutions**:

```python
# 1. Configure aggressive rotation
logger = InsightLogger(
    name="HighVolumeApp",
    max_bytes=10_000_000,   # 10MB files
    backup_count=5,         # Keep only 5 backups
    log_level=logging.WARNING  # Reduce verbosity
)

# 2. Clean up old logs automatically
import os
import time
from pathlib import Path

def cleanup_old_logs(log_dir, max_age_days=30):
    """Remove log files older than max_age_days"""
    log_path = Path(log_dir)
    cutoff_time = time.time() - (max_age_days * 24 * 60 * 60)
    
    for log_file in log_path.glob("*.log*"):
        if log_file.stat().st_mtime < cutoff_time:
            print(f"Removing old log file: {log_file}")
            log_file.unlink()

# Run cleanup weekly
cleanup_old_logs(".insight", max_age_days=30)

# 3. Compress old logs
import gzip
import shutil

def compress_old_logs(log_dir):
    """Compress old log files"""
    log_path = Path(log_dir)
    
    for log_file in log_path.glob("*.log.[1-9]*"):
        if not str(log_file).endswith('.gz'):
            print(f"Compressing: {log_file}")
            with open(log_file, 'rb') as f_in:
                with gzip.open(f"{log_file}.gz", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            log_file.unlink()  # Remove original

compress_old_logs(".insight")
```

## 🔍 Diagnostic Tools

### 1. Logger Health Check

```python
import os
import sqlite3
import smtplib
from insightlog import InsightLogger

def comprehensive_health_check():
    """Comprehensive health check for InsightLogger"""
    print("🔍 InsightLogger Health Check")
    print("=" * 50)
    
    # 1. Basic import test
    try:
        logger = InsightLogger("HealthCheck", save_log="disabled", enable_database=False)
        print("✅ Import and basic initialization: OK")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return
    
    # 2. File system test
    try:
        test_logger = InsightLogger("FileTest", log_dir="./test_logs")
        test_logger.log_types("INFO", "File system test")
        print("✅ File system access: OK")
        
        # Cleanup
        import shutil
        if os.path.exists("./test_logs"):
            shutil.rmtree("./test_logs")
    except Exception as e:
        print(f"❌ File system access failed: {e}")
    
    # 3. Database test
    try:
        db_logger = InsightLogger("DBTest", enable_database=True, save_log="disabled")
        db_logger.log_types("INFO", "Database test")
        logs = db_logger.query_logs(limit=1)
        assert len(logs) > 0
        print("✅ Database functionality: OK")
        db_logger.close_database()
    except Exception as e:
        print(f"❌ Database functionality failed: {e}")
    
    # 4. Monitoring test
    try:
        monitor_logger = InsightLogger("MonitorTest", enable_monitoring=True, save_log="disabled", enable_database=False)
        import time
        time.sleep(2)  # Let monitoring collect some data
        monitor_logger.stop_monitoring()
        print("✅ Monitoring functionality: OK")
    except Exception as e:
        print(f"❌ Monitoring functionality failed: {e}")
    
    # 5. Performance test
    try:
        perf_logger = InsightLogger("PerfTest", save_log="disabled", enable_database=False, enable_monitoring=False)
        start_time = time.time()
        for i in range(100):
            perf_logger.log_types("INFO", f"Performance test {i}")
        elapsed = time.time() - start_time
        
        if elapsed < 1.0:  # Should complete in under 1 second
            print(f"✅ Performance test: OK ({elapsed:.3f}s for 100 logs)")
        else:
            print(f"⚠️  Performance test: SLOW ({elapsed:.3f}s for 100 logs)")
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
    
    print("=" * 50)
    print("Health check completed!")

# Run health check
comprehensive_health_check()
```

### 2. Configuration Validator

```python
def validate_logger_config(**config):
    """Validate logger configuration before creation"""
    errors = []
    warnings = []
    
    # Required fields
    if 'name' not in config:
        errors.append("Missing required field: 'name'")
    
    # Email configuration validation
    if config.get('enable_alerts', False):
        required_email_fields = ['alert_email', 'smtp_server', 'smtp_user', 'smtp_password']
        for field in required_email_fields:
            if not config.get(field):
                errors.append(f"Missing required email field: '{field}'")
    
    # File system validation
    log_dir = config.get('log_dir', '.insight')
    if not os.access(os.path.dirname(log_dir) or '.', os.W_OK):
        errors.append(f"No write permission for log directory: {log_dir}")
    
    # Size validation
    max_bytes = config.get('max_bytes', 1000000)
    if max_bytes <= 0:
        errors.append("max_bytes must be positive")
    
    if max_bytes > 1000000000:  # 1GB
        warnings.append("max_bytes is very large (>1GB), consider smaller values")
    
    backup_count = config.get('backup_count', 1)
    if backup_count < 0:
        errors.append("backup_count cannot be negative")
    
    # Print results
    if errors:
        print("❌ Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print("⚠️  Configuration Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not errors and not warnings:
        print("✅ Configuration is valid!")
    
    return len(errors) == 0

# Test configuration
config = {
    'name': 'TestApp',
    'enable_alerts': True,
    'alert_email': 'admin@company.com',
    'smtp_server': 'smtp.gmail.com',
    'smtp_user': 'alerts@company.com',
    'smtp_password': 'password',
    'max_bytes': 10000000,
    'backup_count': 5
}

validate_logger_config(**config)
```

### 3. Environment Information

```python
def print_environment_info():
    """Print environment information for debugging"""
    import sys
    import platform
    import os
    
    print("🖥️  Environment Information")
    print("=" * 50)
    print(f"Python Version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.architecture()}")
    print(f"Current Working Directory: {os.getcwd()}")
    print(f"Python Path: {sys.path[:3]}...")  # First 3 entries
    
    # Check available packages
    try:
        import matplotlib
        print(f"Matplotlib: {matplotlib.__version__}")
    except ImportError:
        print("Matplotlib: Not installed")
    
    try:
        import plotly
        print(f"Plotly: {plotly.__version__}")
    except ImportError:
        print("Plotly: Not installed")
    
    try:
        import psutil
        print(f"Psutil: {psutil.__version__}")
    except ImportError:
        print("Psutil: Not installed")
    
    # System resources
    try:
        import psutil
        print(f"Available Memory: {psutil.virtual_memory().available / 1024 / 1024:.0f} MB")
        print(f"CPU Count: {psutil.cpu_count()}")
        print(f"Disk Free Space: {psutil.disk_usage('.').free / 1024 / 1024 / 1024:.1f} GB")
    except ImportError:
        print("System resource info: psutil not available")
    
    print("=" * 50)

print_environment_info()
```

## 🚨 Emergency Recovery

### Database Recovery

```python
def emergency_database_recovery(log_dir=".insight"):
    """Emergency database recovery procedure"""
    db_path = os.path.join(log_dir, "insights_session.db")
    
    if not os.path.exists(db_path):
        print("No database file found")
        return
    
    # Backup corrupted database
    backup_path = f"{db_path}.corrupted.{int(time.time())}"
    shutil.copy2(db_path, backup_path)
    print(f"Corrupted database backed up to: {backup_path}")
    
    # Try to recover data
    recovered_data = []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Try to extract logs
        cursor.execute("SELECT * FROM logs")
        recovered_data = cursor.fetchall()
        conn.close()
        print(f"Recovered {len(recovered_data)} log entries")
    except Exception as e:
        print(f"Data recovery failed: {e}")
    
    # Remove corrupted database
    os.remove(db_path)
    
    # Create new logger and restore data
    logger = InsightLogger("Recovery", log_dir=log_dir, enable_database=True)
    
    for row in recovered_data:
        try:
            # Restore log entry (adjust based on schema)
            logger.log_types("INFO", f"RECOVERED: {row[3]}")  # Assuming message is at index 3
        except Exception as e:
            print(f"Failed to restore entry: {e}")
    
    print("Database recovery completed")
    return logger

# Run recovery if needed
# emergency_database_recovery()
```

### Log File Recovery

```python
def recover_log_files(log_dir=".insight"):
    """Recover from corrupted log files"""
    log_files = []
    
    # Find all log files
    for file in os.listdir(log_dir):
        if file.endswith('.log') or '.log.' in file:
            log_files.append(os.path.join(log_dir, file))
    
    for log_file in log_files:
        try:
            # Test file readability
            with open(log_file, 'r', encoding='utf-8') as f:
                f.read(100)  # Try to read first 100 characters
            print(f"✅ {log_file}: OK")
        except Exception as e:
            print(f"❌ {log_file}: {e}")
            
            # Move corrupted file
            backup_name = f"{log_file}.corrupted.{int(time.time())}"
            os.rename(log_file, backup_name)
            print(f"Corrupted file moved to: {backup_name}")

# Run log file recovery
# recover_log_files()
```

---

## 📞 Getting Help

### 1. Enable Debug Logging

```python
import logging

# Enable debug logging for troubleshooting
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create logger with debugging
logger = InsightLogger("DebugApp")
```

### 2. Create Minimal Reproduction

```python
# Minimal example for bug reports
from insightlog import InsightLogger

def minimal_reproduction():
    """Minimal code to reproduce the issue"""
    try:
        logger = InsightLogger("MinimalTest")
        logger.log_types("INFO", "Test message")
        print("SUCCESS: No issues found")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

minimal_reproduction()
```

### 3. System Information for Bug Reports

```python
def generate_bug_report():
    """Generate system information for bug reports"""
    import sys
    import platform
    import os
    
    report = f"""
# Bug Report Information

## Environment
- Python Version: {sys.version}
- Platform: {platform.platform()}
- Working Directory: {os.getcwd()}

## Error Details
(Paste error message and traceback here)

## Minimal Reproduction Code
(Paste minimal code that reproduces the issue)

## Expected Behavior
(Describe what you expected to happen)

## Actual Behavior
(Describe what actually happened)
"""
    
    print(report)
    
    # Save to file
    with open("bug_report.md", "w") as f:
        f.write(report)
    
    print("Bug report template saved to bug_report.md")

# Generate bug report template
# generate_bug_report()
```

---

## 📚 Related Documentation

- [Installation Guide](installation.md)
- [Configuration Guide](configuration.md)
- [Best Practices](best-practices.md)
- [API Reference](api-reference.md)

---

**Most issues can be resolved with proper configuration and environment setup!** 🔧✨

If you're still experiencing issues after following this guide, consider creating a minimal reproduction case and reporting the issue.
