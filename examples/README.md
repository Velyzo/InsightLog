# InsightLogger v1.4 - Examples Documentation

This directory contains comprehensive examples demonstrating all the powerful features of InsightLogger v1.4. Each example is designed to showcase different aspects and use cases of the enhanced logging and monitoring library.

## 📁 Example Files

### 🔧 `basic_examples.py`
**Comprehensive demonstration of core InsightLogger features**

- **Basic Logging**: All log levels with enhanced formatting
- **Advanced Features**: Performance profiling, custom metrics, security events
- **Decorator Examples**: Function timing and monitoring decorators
- **Export & Analysis**: Data export and comprehensive reporting

**Run with:**
```bash
python examples/basic_examples.py
```

**What you'll see:**
- Beautiful colored console output with emojis
- Real-time performance monitoring
- System resource tracking
- Comprehensive analytics and insights
- Generated charts and HTML dashboard

---

### 🌐 `flask_integration.py`
**Complete Flask web application with InsightLogger integration**

- **API Monitoring**: Automatic endpoint performance tracking
- **Security Logging**: Built-in security event monitoring
- **Health Checks**: Comprehensive application health monitoring
- **Error Handling**: Advanced error tracking and reporting
- **Background Tasks**: Continuous metrics collection

**Run with:**
```bash
python examples/flask_integration.py
```

**Available endpoints:**
- `GET /api/health` - Health check with comprehensive monitoring
- `GET /api/users` - User retrieval with performance tracking
- `POST /api/data` - Data creation with validation monitoring
- `POST /api/login` - Login with security event logging
- `GET /api/report` - Heavy processing simulation
- `GET /admin/insights` - Admin analytics dashboard

**Test the API:**
```bash
# Health check
curl http://localhost:5000/api/health

# Get users
curl http://localhost:5000/api/users

# Create data
curl -X POST http://localhost:5000/api/data \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "value": 123}'

# Login
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Admin insights (requires authorization)
curl http://localhost:5000/admin/insights \
  -H "Authorization: Bearer admin_token"
```

---

### 🔬 `data_science_pipeline.py`
**Complete data science and machine learning pipeline monitoring**

- **Data Pipeline Monitoring**: Track data loading, cleaning, and processing
- **Feature Engineering**: Monitor feature creation and validation
- **Model Training**: Track ML model training with performance metrics
- **Model Evaluation**: Monitor cross-validation and model comparison
- **Production Monitoring**: Simulate production ML model monitoring
- **Drift Detection**: Data and concept drift monitoring simulation

**Run with:**
```bash
python examples/data_science_pipeline.py
```

**Features demonstrated:**
- Data quality monitoring and metrics
- Feature engineering validation
- Model performance comparison
- Production deployment simulation
- Anomaly detection in ML pipelines
- Comprehensive analytics for data science workflows

**Note:** Requires `numpy` and `pandas`:
```bash
pip install numpy pandas
```

---

### 🧪 `test_all_features.py`
**Comprehensive test suite for all InsightLogger v1.4 features**

- **Basic Functionality Tests**: Core logging and formatting features
- **Enhanced Features Tests**: Database, monitoring, analytics
- **Export & Visualization Tests**: Data export and dashboard creation
- **Context Manager Tests**: Proper resource cleanup and exception handling
- **Decorator Tests**: Function monitoring and security decorators
- **Database Tests**: SQLite integration and querying
- **Error Handling Tests**: Edge cases and error scenarios
- **Performance Tests**: Memory usage and execution speed validation

**Run with:**
```bash
python examples/test_all_features.py
```

**Test results will show:**
- ✅ Passed tests with feature confirmations
- ❌ Failed tests with error details
- 📊 Overall success rate and summary
- 🧹 Automatic cleanup of test files

---

## 🚀 Quick Start Guide

### 1. Run Basic Examples
Start with the basic examples to understand core features:
```bash
cd InsightLog
python examples/basic_examples.py
```

### 2. Test All Features
Verify everything works correctly:
```bash
python examples/test_all_features.py
```

### 3. Try Flask Integration
See real-world web application monitoring:
```bash
python examples/flask_integration.py
# In another terminal, test the endpoints with curl
```

### 4. Explore Data Science Pipeline
For ML and data science workflows:
```bash
pip install numpy pandas
python examples/data_science_pipeline.py
```

## 📊 Generated Output Files

After running examples, check the `.insight` directory for:

### 📈 Visualizations
- `log_frequency_[timestamp].png` - Log level distribution charts
- `system_metrics_[timestamp].png` - CPU and memory usage over time
- `function_performance_[timestamp].png` - Function execution analysis

### 🌐 Interactive Dashboards
- `dashboard_[session_id].html` - Real-time monitoring dashboard
- Open in browser for interactive charts and metrics

### 🗄️ Data Files
- `insights_[session_id].db` - SQLite database with all metrics
- `insight_export_[timestamp].json` - Comprehensive data export
- `insight_export_[timestamp].csv` - CSV format for analysis
- `app.log` - Traditional log file with enhanced formatting

### 📋 Reports
- Console output with comprehensive analysis
- Health scores and optimization recommendations
- Anomaly detection results
- Performance bottleneck identification

## 🎛️ Configuration Examples

### Basic Configuration
```python
from insightlog import InsightLogger

# Minimal setup
logger = InsightLogger("MyApp")
```

### Production Configuration
```python
# Production-ready configuration
logger = InsightLogger(
    name="ProductionApp",
    enable_database=True,
    enable_monitoring=True,
    enable_alerts=True,
    alert_email="ops@company.com",
    smtp_server="smtp.company.com",
    smtp_user="alerts@company.com",
    smtp_password="secure_password",
    log_level=logging.INFO
)
```

### Development Configuration
```python
# Development with full monitoring
logger = InsightLogger(
    name="DevApp",
    enable_database=True,
    enable_monitoring=True,
    enable_alerts=False,
    log_level=logging.DEBUG
)
```

## 🔧 Customization Examples

### Custom Alert Thresholds
```python
logger = InsightLogger("MyApp", enable_alerts=True)
logger.alert_thresholds = {
    'cpu_usage': 75,        # Alert at 75% CPU
    'memory_usage': 80,     # Alert at 80% memory
    'error_rate': 5,        # Alert at 5% error rate
    'response_time': 2000   # Alert at 2 second response time
}
```

### Custom Metrics Tracking
```python
# Track business metrics
logger.add_custom_metric("daily_active_users", 1500)
logger.add_custom_metric("revenue_today", 25000.50)
logger.add_custom_metric("conversion_rate", 0.034)

# Track system metrics
logger.add_custom_metric("cache_hit_rate", 0.95)
logger.add_custom_metric("database_connections", 45)
logger.add_custom_metric("queue_size", 12)
```

### Security Event Monitoring
```python
# Log security events
logger.log_security_event("LOGIN_ATTEMPT", "LOW", "User login from new IP")
logger.log_security_event("FAILED_LOGIN", "MEDIUM", "Multiple failed attempts")
logger.log_security_event("PRIVILEGE_ESCALATION", "HIGH", "Unauthorized access")
```

## 🎯 Use Case Examples

### 1. **Web API Monitoring**
Perfect for REST APIs, GraphQL services, and microservices:
- Automatic endpoint performance tracking
- Request/response monitoring
- Error rate analysis
- Security event detection

### 2. **Data Processing Pipelines**
Ideal for ETL processes, data science workflows:
- Data quality monitoring
- Processing step performance
- Error tracking and recovery
- Resource usage optimization

### 3. **Machine Learning Operations**
Comprehensive MLOps monitoring:
- Model training performance
- Prediction latency tracking
- Model drift detection
- A/B testing analytics

### 4. **Background Services**
Monitor scheduled jobs, workers, and daemons:
- Task completion tracking
- Resource usage monitoring
- Error rate analysis
- Performance optimization

### 5. **Development & Debugging**
Enhanced development experience:
- Function-level performance profiling
- Memory leak detection
- Bottleneck identification
- Comprehensive debugging information

## 📚 Learning Path

### Beginner
1. Run `basic_examples.py` to understand core concepts
2. Experiment with different log levels and formatting
3. Try the function timing decorator

### Intermediate
1. Run `test_all_features.py` to see all capabilities
2. Explore custom metrics and security events
3. Try the Flask integration example

### Advanced
1. Study the data science pipeline example
2. Implement custom monitoring for your specific use case
3. Set up production monitoring with alerts and dashboards

## 🆘 Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Make sure you're in the InsightLog directory
cd InsightLog
python examples/basic_examples.py
```

**Missing Dependencies:**
```bash
# Install all dependencies
pip install -r requirements.txt

# For data science examples
pip install numpy pandas
```

**Permission Errors:**
```bash
# Make sure the script is executable
chmod +x examples/test_all_features.py
```

**Port Already in Use (Flask example):**
```python
# Change the port in flask_integration.py
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

### Getting Help

1. **Check the main README.md** for comprehensive documentation
2. **Run the test suite** to verify your installation
3. **Look at the generated `.insight` directory** for output files
4. **Check the console output** for detailed error messages

## 🎉 Next Steps

After running the examples:

1. **Integrate InsightLogger** into your own projects
2. **Customize the configuration** for your specific needs
3. **Set up production monitoring** with alerts and dashboards
4. **Explore the generated data** in the SQLite database
5. **Share your insights** and contribute improvements

Remember: InsightLogger v1.4 is designed to be **backward compatible**, so you can start with basic logging and gradually enable more advanced features as needed!
