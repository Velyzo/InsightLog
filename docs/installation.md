# Installation Guide

## 📦 Quick Installation

Install InsightLogger using pip:

```bash
pip install insightlog
```

## 🛠️ Development Installation

For the latest features and development version:

```bash
# Clone the repository
git clone https://github.com/Velyzo/InsightLog.git
cd InsightLog

# Install in development mode
pip install -e .
```

## 📋 Requirements

### System Requirements
- **Python**: 3.9 or higher
- **Operating System**: Windows, macOS, Linux
- **Memory**: Minimum 512MB RAM
- **Storage**: 50MB free space

### Python Dependencies

InsightLogger automatically installs the following dependencies:

#### Core Dependencies
```
termcolor>=2.0.0      # Enhanced terminal colors
matplotlib>=3.5.0     # Plotting and visualization
tabulate>=0.9.0       # Table formatting
psutil>=5.8.0         # System monitoring
numpy>=1.21.0         # Numerical computing
tqdm>=4.64.0          # Progress bars
```

#### Optional Dependencies
For advanced features, you may need additional packages:

```bash
# For web framework integration
pip install flask django fastapi

# For database backends
pip install sqlalchemy pymongo redis

# For cloud integration
pip install boto3 azure-storage-blob google-cloud-storage

# For advanced analytics
pip install pandas scipy scikit-learn
```

## 🔧 Installation Options

### Standard Installation
```bash
pip install insightlog
```
Includes all core features for logging, monitoring, and basic analytics.

### Full Installation
```bash
pip install insightlog[full]
```
Includes all optional dependencies for maximum functionality.

### Minimal Installation
```bash
pip install insightlog[minimal]
```
Installs only the essential dependencies for basic logging.

### Development Installation
```bash
git clone https://github.com/Velyzo/InsightLog.git
cd InsightLog
pip install -e .[dev]
```
Includes development tools, testing frameworks, and documentation generators.

## 🐳 Docker Installation

### Using Pre-built Image
```bash
docker pull velyzo/insightlogger:latest
docker run -it velyzo/insightlogger:latest
```

### Building from Source
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e .

CMD ["python", "-c", "from insightlog import InsightLogger; print('InsightLogger ready!')"]
```

## 🚀 Verification

Verify your installation:

```python
import insightlog
from insightlog import InsightLogger

# Check version
print(f"InsightLogger version: {insightlog.__version__}")

# Create a test logger
logger = InsightLogger("test")
logger.log_types("SUCCESS", "Installation verified!", emoji=True)

# Check available features
features = logger.get_available_features()
print("Available features:", features)
```

Expected output:
```
InsightLogger version: 1.4.0
✅ SUCCESS - Installation verified!
Available features: ['logging', 'monitoring', 'analytics', 'visualization', 'database']
```

## 🔍 Troubleshooting

### Common Issues

#### ImportError: No module named 'insightlog'
```bash
# Solution: Reinstall with --force-reinstall
pip install --force-reinstall insightlog
```

#### Permission denied during installation
```bash
# Solution: Use --user flag
pip install --user insightlog
```

#### Dependency conflicts
```bash
# Solution: Use virtual environment
python -m venv insightlog_env
source insightlog_env/bin/activate  # On Windows: insightlog_env\Scripts\activate
pip install insightlog
```

#### matplotlib/numpy issues
```bash
# Solution: Install with conda
conda install -c conda-forge matplotlib numpy
pip install insightlog
```

### Platform-Specific Notes

#### Windows
- Ensure you have Visual C++ Build Tools installed
- Use PowerShell or Command Prompt as administrator if needed
- Some features may require Windows 10 or later

#### macOS
- Xcode Command Line Tools may be required: `xcode-select --install`
- For M1 Macs, ensure compatibility with arm64 architecture

#### Linux
- Install development headers: `sudo apt-get install python3-dev`
- For RedHat/CentOS: `sudo yum install python3-devel`

## 🧪 Testing Installation

Run the comprehensive test suite:

```python
from insightlog import InsightLogger

def test_installation():
    """Test all major features to ensure proper installation"""
    print("🧪 Testing InsightLogger installation...")
    
    # Test 1: Basic logging
    logger = InsightLogger("InstallTest")
    logger.log_types("INFO", "Testing basic logging")
    print("✅ Basic logging works")
    
    # Test 2: Performance monitoring
    @logger.log_function_time
    def test_function():
        import time
        time.sleep(0.1)
        return "test"
    
    result = test_function()
    print("✅ Performance monitoring works")
    
    # Test 3: System monitoring
    if logger.enable_monitoring:
        print("✅ System monitoring enabled")
    
    # Test 4: Database functionality
    if hasattr(logger, 'conn'):
        print("✅ Database integration works")
    
    # Test 5: Visualization
    try:
        import matplotlib
        print("✅ Visualization support available")
    except ImportError:
        print("⚠️ Visualization support limited (matplotlib not found)")
    
    # Test 6: Export functionality
    data = logger.export_data("json")
    if data:
        print("✅ Export functionality works")
    
    logger.stop_monitoring()
    print("🎉 Installation test completed successfully!")

if __name__ == "__main__":
    test_installation()
```

## 🔄 Updating

### Update to Latest Version
```bash
pip install --upgrade insightlog
```

### Update Development Version
```bash
cd InsightLogger
git pull origin main
pip install -e . --upgrade
```

### Version History
Check what's new in each version:

```python
from insightlog import InsightLogger
logger = InsightLogger("version_check")
logger.show_version_info()
```

## 🎯 Next Steps

After successful installation:

1. **[Quick Start Tutorial](quickstart.md)** - Build your first application
2. **[Basic Examples](basic-examples.md)** - Explore code examples
3. **[Configuration Guide](configuration.md)** - Customize settings
4. **[API Reference](api-reference.md)** - Detailed API documentation

---

**Need Help?** 
- 📧 Email: help@velyzo.de
- 🐛 Issues: [GitHub Issues](https://github.com/Velyzo/InsightLog/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/Velyzo/InsightLog/discussions)
