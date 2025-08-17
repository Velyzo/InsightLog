# Best Practices Guide

Comprehensive guide to using InsightLogger effectively in production environments and following industry standards.

## 🎯 General Best Practices

### 1. Application Design Principles

#### Initialize Once, Use Everywhere

```python
# ✅ Good: Singleton pattern
class LoggerManager:
    _instance = None
    _logger = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_logger(self):
        if self._logger is None:
            self._logger = InsightLogger(
                name="ProductionApp",
                log_level=logging.INFO,
                enable_database=True,
                enable_monitoring=True
            )
        return self._logger

# Usage
logger_manager = LoggerManager()
logger = logger_manager.get_logger()
```

```python
# ❌ Avoid: Multiple instances
def bad_function():
    logger = InsightLogger("BadExample")  # Creates new instance each time
    logger.log_types("INFO", "This is wasteful")
```

#### Proper Resource Management

```python
# ✅ Good: Context manager usage
from contextlib import contextmanager

@contextmanager
def managed_logger(name, **kwargs):
    logger = InsightLogger(name, **kwargs)
    try:
        yield logger
    finally:
        logger.stop_monitoring()
        logger.close_database()

# Usage
with managed_logger("TemporaryTask") as logger:
    logger.log_types("INFO", "Task started")
    # ... do work ...
    logger.log_types("INFO", "Task completed")
# Resources automatically cleaned up
```

### 2. Logging Strategy

#### Structured Logging

```python
# ✅ Good: Structured and consistent
def process_user_request(user_id, action, data):
    context = {
        "user_id": user_id,
        "action": action,
        "request_size": len(str(data)),
        "timestamp": datetime.now().isoformat()
    }
    
    logger.log_context(
        "INFO", 
        f"Processing user request: {action}", 
        context
    )
    
    try:
        result = perform_action(action, data)
        logger.log_context(
            "INFO",
            f"Request completed successfully: {action}",
            {**context, "result_size": len(str(result))}
        )
        return result
    except Exception as e:
        logger.log_context(
            "ERROR",
            f"Request failed: {action}",
            {**context, "error": str(e)}
        )
        raise
```

#### Log Levels Usage

```python
# ✅ Good: Appropriate log levels
class PaymentProcessor:
    def __init__(self):
        self.logger = LoggerManager().get_logger()
    
    def process_payment(self, amount, card_info):
        # DEBUG: Detailed information for debugging
        self.logger.log_types("DEBUG", f"Processing payment of ${amount}")
        
        # INFO: Important business events
        self.logger.log_types("INFO", f"Payment initiated: ${amount}")
        
        try:
            # Validate card
            if not self.validate_card(card_info):
                # WARNING: Potential issues that don't prevent operation
                self.logger.log_types("WARNING", "Invalid card format, but retrying")
                card_info = self.normalize_card(card_info)
            
            # Process payment
            result = self.charge_card(amount, card_info)
            
            # INFO: Successful business events
            self.logger.log_types("INFO", f"Payment successful: ${amount}, ID: {result.id}")
            
            return result
            
        except PaymentDeclinedException as e:
            # WARNING: Expected business exceptions
            self.logger.log_types("WARNING", f"Payment declined: {e.reason}")
            raise
            
        except PaymentGatewayException as e:
            # ERROR: Unexpected technical issues
            self.logger.log_types("ERROR", f"Payment gateway error: {e}")
            raise
            
        except Exception as e:
            # CRITICAL: Unexpected system failures
            self.logger.log_types("CRITICAL", f"Unexpected payment error: {e}")
            raise
```

## 🚀 Performance Best Practices

### 1. Efficient Logging

#### Lazy String Formatting

```python
# ✅ Good: Lazy evaluation
def expensive_operation(data):
    # Only format string if DEBUG level is enabled
    logger.log_types("DEBUG", f"Processing data: {expensive_data_repr(data)}")
    
    # Even better: Check log level first
    if logger.logger.isEnabledFor(logging.DEBUG):
        logger.log_types("DEBUG", f"Processing data: {expensive_data_repr(data)}")

# ❌ Avoid: Always formatting expensive strings
def bad_operation(data):
    expensive_string = expensive_data_repr(data)  # Always computed
    logger.log_types("DEBUG", f"Processing data: {expensive_string}")
```

#### Batch Operations

```python
# ✅ Good: Batch database operations
class BulkLogger:
    def __init__(self):
        self.logger = InsightLogger("BulkApp", enable_database=True)
        self.pending_logs = []
        self.batch_size = 100
    
    def add_log(self, level, message, context=None):
        self.pending_logs.append({
            'level': level,
            'message': message,
            'context': context,
            'timestamp': datetime.now()
        })
        
        if len(self.pending_logs) >= self.batch_size:
            self.flush_logs()
    
    def flush_logs(self):
        for log_entry in self.pending_logs:
            self.logger.log_context(
                log_entry['level'],
                log_entry['message'],
                log_entry['context']
            )
        self.pending_logs.clear()
```

### 2. Memory Management

#### Memory-Efficient Monitoring

```python
# ✅ Good: Configure monitoring intervals
logger = InsightLogger(
    name="HighVolumeApp",
    enable_monitoring=True
)

# Adjust monitoring frequency for high-volume applications
logger.monitoring_interval = 5  # Collect metrics every 5 seconds instead of 1
```

#### Log Rotation Configuration

```python
# ✅ Good: Appropriate log rotation
logger = InsightLogger(
    name="ProductionApp",
    max_bytes=50_000_000,    # 50MB files
    backup_count=10,         # Keep 10 backups (500MB total)
    log_dir="/var/log/myapp"
)

# For high-volume applications
high_volume_logger = InsightLogger(
    name="HighVolumeApp",
    max_bytes=100_000_000,   # 100MB files
    backup_count=5,          # Keep 5 backups (500MB total)
    log_level=logging.INFO   # Reduce verbosity
)
```

## 🔒 Security Best Practices

### 1. Sensitive Data Handling

#### Data Sanitization

```python
import re
from typing import Dict, Any

class SecureLogger:
    def __init__(self):
        self.logger = InsightLogger("SecureApp", enable_database=True)
        self.sensitive_patterns = [
            (re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'), '[CARD_REDACTED]'),
            (re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'), '[EMAIL_REDACTED]'),
            (re.compile(r'\b\d{3}-\d{2}-\d{4}\b'), '[SSN_REDACTED]'),
            (re.compile(r'password["\']?\s*[:=]\s*["\']?([^"\'\\s]+)', re.IGNORECASE), 'password=[REDACTED]')
        ]
    
    def sanitize_message(self, message: str) -> str:
        """Remove sensitive data from log messages"""
        for pattern, replacement in self.sensitive_patterns:
            message = pattern.sub(replacement, message)
        return message
    
    def sanitize_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Remove sensitive data from context"""
        if not context:
            return context
        
        sanitized = {}
        sensitive_keys = {'password', 'token', 'secret', 'key', 'auth', 'credential'}
        
        for key, value in context.items():
            if any(sensitive_key in key.lower() for sensitive_key in sensitive_keys):
                sanitized[key] = '[REDACTED]'
            elif isinstance(value, str):
                sanitized[key] = self.sanitize_message(value)
            else:
                sanitized[key] = value
        
        return sanitized
    
    def secure_log(self, level: str, message: str, context: Dict[str, Any] = None):
        """Log with automatic data sanitization"""
        clean_message = self.sanitize_message(message)
        clean_context = self.sanitize_context(context)
        
        self.logger.log_context(level, clean_message, clean_context)
```

### 2. Access Control

#### Secure File Permissions

```python
import os
import stat

def setup_secure_logging():
    log_dir = "/var/log/myapp"
    
    # Create directory with restricted permissions
    os.makedirs(log_dir, mode=0o750, exist_ok=True)  # rwxr-x---
    
    logger = InsightLogger(
        name="SecureApp",
        log_dir=log_dir,
        enable_database=True
    )
    
    # Set restrictive permissions on log files
    log_file = os.path.join(log_dir, "app.log")
    if os.path.exists(log_file):
        os.chmod(log_file, 0o640)  # rw-r-----
    
    # Set restrictive permissions on database
    db_file = os.path.join(log_dir, "insights_session.db")
    if os.path.exists(db_file):
        os.chmod(db_file, 0o640)  # rw-r-----
    
    return logger
```

### 3. Authentication & Credentials

#### Secure SMTP Configuration

```python
import os
from cryptography.fernet import Fernet

class SecureEmailConfig:
    def __init__(self):
        self.encryption_key = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
        self.cipher = Fernet(self.encryption_key)
    
    def encrypt_password(self, password: str) -> str:
        return self.cipher.encrypt(password.encode()).decode()
    
    def decrypt_password(self, encrypted_password: str) -> str:
        return self.cipher.decrypt(encrypted_password.encode()).decode()
    
    def get_secure_logger(self):
        # Use environment variables for sensitive config
        encrypted_password = os.getenv('SMTP_PASSWORD_ENCRYPTED')
        
        if encrypted_password:
            smtp_password = self.decrypt_password(encrypted_password)
        else:
            smtp_password = os.getenv('SMTP_PASSWORD')  # Fallback
        
        return InsightLogger(
            name="SecureApp",
            enable_alerts=True,
            alert_email=os.getenv('ALERT_EMAIL'),
            smtp_server=os.getenv('SMTP_SERVER'),
            smtp_port=int(os.getenv('SMTP_PORT', 587)),
            smtp_user=os.getenv('SMTP_USER'),
            smtp_password=smtp_password
        )
```

## 🏗️ Architecture Best Practices

### 1. Microservices Architecture

#### Service-Specific Loggers

```python
# Each microservice has its own logger configuration
class UserServiceLogger:
    def __init__(self):
        self.logger = InsightLogger(
            name="UserService",
            log_dir="/var/log/microservices/user-service",
            enable_database=True,
            enable_monitoring=True,
            enable_alerts=True,
            alert_email="user-service-alerts@company.com"
        )
    
    def log_user_action(self, user_id: str, action: str, details: dict = None):
        context = {
            "service": "user-service",
            "user_id": user_id,
            "action": action,
            "details": details or {}
        }
        self.logger.log_context("INFO", f"User action: {action}", context)

class OrderServiceLogger:
    def __init__(self):
        self.logger = InsightLogger(
            name="OrderService",
            log_dir="/var/log/microservices/order-service",
            enable_database=True,
            enable_monitoring=True,
            enable_alerts=True,
            alert_email="order-service-alerts@company.com"
        )
    
    def log_order_event(self, order_id: str, event: str, details: dict = None):
        context = {
            "service": "order-service",
            "order_id": order_id,
            "event": event,
            "details": details or {}
        }
        self.logger.log_context("INFO", f"Order event: {event}", context)
```

### 2. Distributed Tracing

#### Correlation IDs

```python
import uuid
from contextlib import contextmanager
from contextvars import ContextVar

# Context variable for request tracing
correlation_id: ContextVar[str] = ContextVar('correlation_id')

@contextmanager
def trace_request(request_id: str = None):
    """Context manager for request tracing"""
    if request_id is None:
        request_id = str(uuid.uuid4())
    
    token = correlation_id.set(request_id)
    try:
        yield request_id
    finally:
        correlation_id.reset(token)

class TracingLogger:
    def __init__(self):
        self.logger = InsightLogger("TracingApp", enable_database=True)
    
    def log_with_trace(self, level: str, message: str, context: dict = None):
        """Log with automatic correlation ID"""
        trace_id = correlation_id.get(None)
        
        full_context = {
            "correlation_id": trace_id,
            **(context or {})
        }
        
        self.logger.log_context(level, message, full_context)

# Usage
tracing_logger = TracingLogger()

def process_request(request_data):
    with trace_request() as request_id:
        tracing_logger.log_with_trace("INFO", "Request started", {"data_size": len(request_data)})
        
        # Call other services
        user_data = get_user_data(request_data.user_id)
        tracing_logger.log_with_trace("INFO", "User data retrieved")
        
        result = process_data(user_data, request_data)
        tracing_logger.log_with_trace("INFO", "Request completed", {"result_size": len(result)})
        
        return result
```

## 📊 Monitoring Best Practices

### 1. Health Checks

#### Application Health Monitoring

```python
import psutil
from datetime import datetime, timedelta

class HealthMonitor:
    def __init__(self):
        self.logger = InsightLogger("HealthMonitor", enable_monitoring=True)
        self.last_health_check = datetime.now()
        self.health_check_interval = timedelta(minutes=5)
    
    def check_application_health(self):
        """Comprehensive application health check"""
        now = datetime.now()
        
        if now - self.last_health_check < self.health_check_interval:
            return  # Skip if too soon
        
        self.last_health_check = now
        
        health_data = {
            "timestamp": now.isoformat(),
            "system": self._check_system_health(),
            "application": self._check_application_health(),
            "database": self._check_database_health()
        }
        
        overall_status = self._determine_overall_health(health_data)
        
        self.logger.log_context(
            "INFO" if overall_status == "healthy" else "WARNING",
            f"Health check completed: {overall_status}",
            health_data
        )
        
        if overall_status != "healthy":
            self._send_health_alert(health_data)
    
    def _check_system_health(self):
        """Check system resource health"""
        return {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "load_average": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
        }
    
    def _check_application_health(self):
        """Check application-specific health"""
        try:
            # Check if key application components are working
            self._test_core_functionality()
            return {"status": "healthy", "message": "All components operational"}
        except Exception as e:
            return {"status": "unhealthy", "message": str(e)}
    
    def _check_database_health(self):
        """Check database connectivity and performance"""
        try:
            start_time = datetime.now()
            logs = self.logger.query_logs(limit=1)
            query_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "status": "healthy",
                "query_time_seconds": query_time,
                "responsive": query_time < 1.0
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
```

### 2. Performance Metrics

#### Custom Metrics Collection

```python
import time
from collections import defaultdict, deque
from threading import Lock

class PerformanceCollector:
    def __init__(self):
        self.logger = InsightLogger("PerformanceApp", enable_database=True)
        self.metrics = defaultdict(deque)
        self.metrics_lock = Lock()
        self.max_samples = 1000  # Keep last 1000 samples
    
    def track_execution_time(self, operation_name: str):
        """Decorator to track execution time"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    self._record_metric(f"{operation_name}_success", execution_time)
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    self._record_metric(f"{operation_name}_error", execution_time)
                    raise
            return wrapper
        return decorator
    
    def _record_metric(self, metric_name: str, value: float):
        """Record a metric value"""
        with self.metrics_lock:
            self.metrics[metric_name].append({
                'timestamp': time.time(),
                'value': value
            })
            
            # Keep only recent samples
            if len(self.metrics[metric_name]) > self.max_samples:
                self.metrics[metric_name].popleft()
        
        # Log to InsightLogger
        self.logger.add_custom_metric(metric_name, value)
    
    def get_metric_stats(self, metric_name: str) -> dict:
        """Get statistics for a metric"""
        with self.metrics_lock:
            samples = self.metrics.get(metric_name, deque())
            
            if not samples:
                return {"count": 0}
            
            values = [sample['value'] for sample in samples]
            
            return {
                "count": len(values),
                "min": min(values),
                "max": max(values),
                "mean": sum(values) / len(values),
                "recent_avg": sum(values[-10:]) / min(len(values), 10)  # Last 10 samples
            }

# Usage
performance = PerformanceCollector()

@performance.track_execution_time("database_query")
def query_database(query):
    # Simulate database query
    time.sleep(0.1)
    return "result"

@performance.track_execution_time("api_call")
def call_external_api(endpoint):
    # Simulate API call
    time.sleep(0.2)
    return "response"
```

## 🧪 Testing Best Practices

### 1. Unit Testing

#### Logger Mocking

```python
import unittest
from unittest.mock import Mock, patch
from insightlog import InsightLogger

class TestLoggerIntegration(unittest.TestCase):
    def setUp(self):
        # Mock logger for testing
        self.mock_logger = Mock(spec=InsightLogger)
        
    def test_business_logic_with_logging(self):
        """Test business logic without actually logging"""
        with patch('myapp.logger', self.mock_logger):
            result = my_business_function("test_data")
            
            # Verify logging calls
            self.mock_logger.log_types.assert_called_with("INFO", "Function completed")
            self.assertEqual(result, "expected_result")
    
    def test_error_logging(self):
        """Test error logging behavior"""
        with patch('myapp.logger', self.mock_logger):
            with self.assertRaises(ValueError):
                my_function_that_raises_error()
            
            # Verify error was logged
            self.mock_logger.log_types.assert_called_with("ERROR", unittest.mock.ANY)

class TestLoggerConfiguration(unittest.TestCase):
    def test_logger_initialization(self):
        """Test logger initializes correctly"""
        logger = InsightLogger(
            name="TestLogger",
            save_log="disabled",  # Don't create files during tests
            enable_database=False,  # Don't create database during tests
            enable_monitoring=False  # Don't start monitoring during tests
        )
        
        self.assertEqual(logger.name, "TestLogger")
        self.assertFalse(logger.enable_database)
```

### 2. Integration Testing

#### Test Logger Setup

```python
import tempfile
import os
from pathlib import Path

class TestLoggerSetup:
    """Helper class for setting up loggers in tests"""
    
    def __init__(self):
        self.temp_dir = None
        self.logger = None
    
    def __enter__(self):
        # Create temporary directory for test logs
        self.temp_dir = tempfile.mkdtemp()
        
        self.logger = InsightLogger(
            name="TestApp",
            log_dir=self.temp_dir,
            enable_database=True,
            enable_monitoring=False,  # Don't start monitoring in tests
            enable_alerts=False  # Don't send emails in tests
        )
        
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.logger:
            self.logger.stop_monitoring()
            self.logger.close_database()
        
        # Clean up temporary files
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)

# Usage in tests
def test_logger_functionality():
    with TestLoggerSetup() as logger:
        logger.log_types("INFO", "Test message")
        
        # Verify log was written
        logs = logger.query_logs(limit=1)
        assert len(logs) == 1
        assert logs[0][3] == "Test message"  # message column
```

## 🔧 Deployment Best Practices

### 1. Environment Configuration

#### Configuration Management

```python
import os
from enum import Enum

class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class LoggerFactory:
    @staticmethod
    def create_logger(app_name: str) -> InsightLogger:
        env = Environment(os.getenv('ENVIRONMENT', 'development'))
        
        if env == Environment.DEVELOPMENT:
            return LoggerFactory._create_dev_logger(app_name)
        elif env == Environment.STAGING:
            return LoggerFactory._create_staging_logger(app_name)
        elif env == Environment.PRODUCTION:
            return LoggerFactory._create_prod_logger(app_name)
    
    @staticmethod
    def _create_dev_logger(app_name: str) -> InsightLogger:
        return InsightLogger(
            name=f"{app_name}_dev",
            log_level=logging.DEBUG,
            enable_database=True,
            enable_monitoring=True,
            enable_alerts=False,
            max_bytes=1_000_000,  # 1MB
            backup_count=2
        )
    
    @staticmethod
    def _create_staging_logger(app_name: str) -> InsightLogger:
        return InsightLogger(
            name=f"{app_name}_staging",
            log_level=logging.INFO,
            enable_database=True,
            enable_monitoring=True,
            enable_alerts=True,
            alert_email=os.getenv('STAGING_ALERT_EMAIL'),
            smtp_server=os.getenv('SMTP_SERVER'),
            smtp_user=os.getenv('SMTP_USER'),
            smtp_password=os.getenv('SMTP_PASSWORD'),
            max_bytes=10_000_000,  # 10MB
            backup_count=5
        )
    
    @staticmethod
    def _create_prod_logger(app_name: str) -> InsightLogger:
        return InsightLogger(
            name=f"{app_name}_prod",
            log_level=logging.WARNING,  # Less verbose in production
            log_dir="/var/log/myapp",
            enable_database=True,
            enable_monitoring=True,
            enable_alerts=True,
            alert_email=os.getenv('PROD_ALERT_EMAIL'),
            smtp_server=os.getenv('SMTP_SERVER'),
            smtp_user=os.getenv('SMTP_USER'),
            smtp_password=os.getenv('SMTP_PASSWORD'),
            max_bytes=50_000_000,  # 50MB
            backup_count=10
        )
```

### 2. Container Deployment

#### Dockerfile Best Practices

```dockerfile
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create log directory with proper permissions
RUN mkdir -p /app/logs && \
    chown -R appuser:appgroup /app/logs && \
    chmod 755 /app/logs

# Switch to non-root user
USER appuser

# Environment configuration
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production
ENV LOG_DIR=/app/logs

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from health_check import check_health; check_health()" || exit 1

CMD ["python", "app.py"]
```

### 3. Monitoring & Alerting

#### Production Monitoring Setup

```python
class ProductionMonitor:
    def __init__(self):
        self.logger = InsightLogger(
            name="ProductionApp",
            enable_monitoring=True,
            enable_alerts=True,
            alert_email="ops@company.com,dev@company.com"
        )
        
        # Configure alert thresholds for production
        self.logger.alert_thresholds = {
            'cpu_usage': 80,
            'memory_usage': 85,
            'disk_usage': 90,
            'error_rate': 5,  # 5% error rate
            'response_time': 2000,  # 2 seconds
            'failed_requests': 10  # 10 failed requests per minute
        }
        
        self.error_count = 0
        self.request_count = 0
        self.last_alert_time = {}
        self.alert_cooldown = 300  # 5 minutes
    
    def log_request(self, endpoint: str, method: str, status_code: int, response_time: float):
        """Log API request with monitoring"""
        self.request_count += 1
        
        if status_code >= 400:
            self.error_count += 1
        
        context = {
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "response_time_ms": response_time,
            "error_rate": (self.error_count / self.request_count) * 100
        }
        
        level = "ERROR" if status_code >= 500 else "WARNING" if status_code >= 400 else "INFO"
        
        self.logger.log_context(
            level,
            f"{method} {endpoint} - {status_code} ({response_time}ms)",
            context
        )
        
        # Check for alerts
        self._check_error_rate_alert(context)
        self._check_response_time_alert(response_time, endpoint)
    
    def _check_error_rate_alert(self, context: dict):
        """Check if error rate exceeds threshold"""
        error_rate = context.get('error_rate', 0)
        threshold = self.logger.alert_thresholds.get('error_rate', 5)
        
        if error_rate > threshold and self.request_count > 10:  # Only after enough samples
            self._send_alert_if_not_recent(
                'error_rate',
                f"High error rate detected: {error_rate:.1f}%",
                context
            )
    
    def _check_response_time_alert(self, response_time: float, endpoint: str):
        """Check if response time exceeds threshold"""
        threshold = self.logger.alert_thresholds.get('response_time', 2000)
        
        if response_time > threshold:
            self._send_alert_if_not_recent(
                f'response_time_{endpoint}',
                f"Slow response time: {response_time:.1f}ms for {endpoint}",
                {"endpoint": endpoint, "response_time": response_time}
            )
    
    def _send_alert_if_not_recent(self, alert_type: str, message: str, context: dict):
        """Send alert if not sent recently (cooldown)"""
        now = time.time()
        last_sent = self.last_alert_time.get(alert_type, 0)
        
        if now - last_sent > self.alert_cooldown:
            self.logger.log_context("CRITICAL", f"ALERT: {message}", context)
            self.last_alert_time[alert_type] = now
```

## 🎉 Success Patterns

### 1. Gradual Rollout

```python
class FeatureLogger:
    """Logger with feature flag support"""
    
    def __init__(self):
        self.logger = InsightLogger("FeatureApp", enable_database=True)
        self.feature_flags = self._load_feature_flags()
    
    def log_feature_usage(self, feature_name: str, user_id: str, success: bool):
        """Log feature usage for analysis"""
        if not self.feature_flags.get(f"log_{feature_name}", True):
            return  # Feature logging disabled
        
        context = {
            "feature": feature_name,
            "user_id": user_id,
            "success": success,
            "rollout_percentage": self.feature_flags.get(f"{feature_name}_rollout", 100)
        }
        
        self.logger.log_context(
            "INFO",
            f"Feature usage: {feature_name}",
            context
        )
    
    def _load_feature_flags(self) -> dict:
        """Load feature flags from configuration"""
        return {
            "log_new_feature": True,
            "new_feature_rollout": 10,  # 10% rollout
            "log_payment_flow": True,
            "payment_flow_rollout": 100
        }
```

### 2. A/B Testing Support

```python
class ABTestLogger:
    """Logger with A/B testing support"""
    
    def log_ab_test_event(self, test_name: str, variant: str, user_id: str, 
                         event_type: str, value: float = None):
        """Log A/B test events"""
        context = {
            "ab_test": test_name,
            "variant": variant,
            "user_id": user_id,
            "event_type": event_type,
            "value": value
        }
        
        self.logger.log_context(
            "INFO",
            f"A/B Test Event: {test_name}/{variant} - {event_type}",
            context
        )
```

---

## 📚 Related Documentation

- [Configuration Guide](configuration.md)
- [API Reference](api-reference.md)
- [Troubleshooting](troubleshooting.md)
- [Performance Tuning](performance-tuning.md)

---

**Following best practices ensures reliable, maintainable, and secure logging!** 🎯✨

These practices will help you build robust applications with comprehensive logging and monitoring capabilities.
