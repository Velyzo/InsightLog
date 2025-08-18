"""
InsightLogger v1.5 - Basic Usage Examples

This file demonstrates the basic usage of InsightLogger with all its enhanced features.
"""

import time
import random
from insightlog import InsightLogger

def basic_logging_example():
    """Demonstrate basic logging features"""
    print("🔍 Basic Logging Features Demo")
    print("=" * 40)
    
    # Initialize logger with basic configuration
    logger = InsightLogger(
        name="BasicDemo",
        enable_database=True,
        enable_monitoring=True
    )
    
    # Basic log levels (professional style by default)
    logger.log_types("INFO", "Application started successfully", bold=True)
    logger.log_types("SUCCESS", "Database connection established", border=True)
    logger.log_types("WARNING", "Configuration file not found, using defaults")
    logger.log_types("ERROR", "Failed to connect to external API", urgent=True)
    logger.log_types("DEBUG", "Processing user request #12345")
    logger.log_types("TRACE", "Entering authentication module")
    logger.log_types("HIGHLIGHT", "Monthly report generated successfully", header=True)
    logger.log_types("CRITICAL", "Database connection lost", urgent=True, bold=True)
    
    # Function timing demo
    @logger.log_function_time
    def simulate_work(duration=2):
        """Simulate some work"""
        time.sleep(duration)
        return f"Work completed in {duration} seconds"
    
    result = simulate_work(1.5)
    logger.log_types("SUCCESS", f"Task result: {result}")
    
    # View basic insights
    logger.view_insights(detailed=False)
    
    # Cleanup
    logger.stop_monitoring()
    print("Basic demo completed!\n")

def emoji_example():
    """Demonstrate emoji usage when enabled"""
    print("Emoji Usage Demo")
    print("=" * 40)
    
    # Logger with emojis enabled
    logger = InsightLogger(
        name="EmojiDemo",
        enable_emojis=True,  # Enable emojis for visual appeal
        enable_database=False,
        enable_monitoring=False
    )
    
    # Log messages with emojis
    logger.log_types("INFO", "Application started with emoji support")
    logger.log_types("SUCCESS", "Task completed successfully")
    logger.log_types("WARNING", "Low disk space warning")
    logger.log_types("ERROR", "Connection timeout occurred")
    
    print("Emoji demo completed!\n")

def advanced_features_example():
    """Demonstrate advanced monitoring and analytics features"""
    print("🚀 Advanced Features Demo")
    print("=" * 40)
    
    # Use context manager for automatic cleanup
    with InsightLogger(
        name="AdvancedDemo",
        enable_database=True,
        enable_monitoring=True,
        enable_alerts=False  # Set to True with email config for real alerts
    ) as logger:
        
        # Performance profiling
        print("📊 Performance Profiling...")
        
        with logger.performance_profile("data_processing"):
            # Simulate data processing
            data = [random.random() for _ in range(100000)]
            processed = [x ** 2 for x in data]
            result = sum(processed)
        
        logger.log_types("SUCCESS", f"Data processing completed, sum: {result:.2f}")
        
        # Custom metrics
        print("📈 Adding Custom Metrics...")
        logger.add_custom_metric("users_online", random.randint(50, 200))
        logger.add_custom_metric("cache_hit_rate", random.uniform(0.8, 0.99))
        logger.add_custom_metric("response_time_avg", random.uniform(100, 500))
        logger.add_custom_metric("database_connections", random.randint(10, 50))
        
        # API monitoring
        print("🌐 API Monitoring...")
        endpoints = ["/api/users", "/api/data", "/api/auth", "/api/reports"]
        for endpoint in endpoints:
            response_time = random.uniform(50, 800)
            status_code = random.choice([200, 200, 200, 201, 400, 404, 500])
            logger.track_api_call(endpoint, "GET", response_time, status_code)
        
        # Security events
        print("🔒 Security Event Logging...")
        security_events = [
            ("LOGIN_ATTEMPT", "LOW", "User login from new device"),
            ("FAILED_LOGIN", "MEDIUM", "Multiple failed login attempts detected"),
            ("API_RATE_LIMIT", "MEDIUM", "Rate limit exceeded for IP 192.168.1.100"),
            ("SUSPICIOUS_ACTIVITY", "HIGH", "Unusual data access pattern detected")
        ]
        
        for event_type, severity, description in security_events:
            logger.log_security_event(event_type, severity, description)
        
        # Contextual logging
        print("🏷️ Contextual Logging...")
        logger.log_with_context(
            "INFO",
            "User performed data export",
            context={
                "user_id": 12345,
                "action": "export_data",
                "ip_address": "192.168.1.50",
                "file_size": "2.3MB",
                "export_format": "CSV"
            },
            tags=["user_activity", "data_export", "audit"]
        )
        
        # Batch logging
        print("📦 Batch Logging...")
        batch_logs = [
            {"level": "INFO", "message": "Processing batch item 1", "bold": True},
            {"level": "INFO", "message": "Processing batch item 2", "bold": True},
            {"level": "SUCCESS", "message": "Batch item 3 completed successfully"},
            ("WARNING", "Batch item 4 took longer than expected"),
            ("INFO", "Batch processing completed")
        ]
        logger.batch_log(batch_logs)
        
        # Simulate some errors for analysis
        print("🐛 Error Simulation...")
        error_scenarios = [
            ("ERROR", "Database timeout occurred"),
            ("WARNING", "Memory usage approaching limit"),
            ("ERROR", "External service unavailable"),
            ("CRITICAL", "Disk space critically low")
        ]
        
        for level, message in error_scenarios:
            logger.log_types(level, message, emoji=True)
        
        # Wait for monitoring data
        print("⏳ Collecting monitoring data...")
        time.sleep(5)
        
        # Generate comprehensive analysis
        print("\n🔍 Generating Comprehensive Analysis...")
        logger.view_insights(
            detailed=True,
            export_format="json",
            create_dashboard=True
        )

def decorator_examples():
    """Demonstrate various decorator usage patterns"""
    print("🎭 Decorator Examples")
    print("=" * 40)
    
    logger = InsightLogger("DecoratorDemo", enable_monitoring=True)
    
    # Standard timing decorator
    @logger.log_function_time
    def calculate_fibonacci(n):
        """Calculate fibonacci number"""
        if n <= 1:
            return n
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
    
    # Error-prone function
    @logger.log_function_time
    def risky_operation():
        """Function that might fail"""
        if random.random() < 0.3:  # 30% chance of failure
            raise ValueError("Random failure occurred")
        time.sleep(random.uniform(0.5, 2.0))
        return "Operation successful"
    
    print("🔢 Fibonacci Calculation...")
    result = calculate_fibonacci(10)
    logger.log_types("SUCCESS", f"Fibonacci(10) = {result}")
    
    print("🎲 Risky Operations...")
    for i in range(5):
        try:
            result = risky_operation()
            logger.log_types("SUCCESS", f"Operation {i+1}: {result}")
        except ValueError as e:
            logger.log_types("ERROR", f"Operation {i+1} failed: {e}")
    
    # View function statistics
    stats = logger.get_function_statistics()
    print("\n📊 Function Statistics:")
    for func_name, metrics in stats.items():
        print(f"  • {func_name}:")
        print(f"    - Calls: {metrics['call_count']}")
        print(f"    - Avg Time: {metrics['avg_time']:.2f}ms")
        print(f"    - Success Rate: {metrics['success_rate']:.1f}%")
    
    logger.stop_monitoring()
    print("\n✅ Decorator demo completed!\n")

def export_and_analysis_example():
    """Demonstrate data export and analysis features"""
    print("📤 Export and Analysis Demo")
    print("=" * 40)
    
    with InsightLogger("ExportDemo", enable_database=True, enable_monitoring=True) as logger:
        
        # Generate some activity
        @logger.log_function_time
        def generate_activity():
            """Generate various types of activity for analysis"""
            
            # Simulate different operations
            operations = ["user_login", "data_query", "report_generation", "file_upload", "cache_update"]
            
            for operation in operations:
                with logger.performance_profile(operation):
                    duration = random.uniform(0.1, 2.0)
                    time.sleep(duration)
                    
                    # Add some custom metrics
                    logger.add_custom_metric(f"{operation}_duration", duration * 1000)
                    logger.add_custom_metric(f"{operation}_success", 1)
                    
                    logger.log_types("INFO", f"Completed {operation}", emoji=True)
        
        print("🔄 Generating Activity...")
        generate_activity()
        
        # Add more custom metrics
        for i in range(10):
            logger.add_custom_metric("concurrent_users", random.randint(50, 150))
            logger.add_custom_metric("memory_usage_mb", random.uniform(512, 1024))
            time.sleep(0.5)
        
        print("📊 Performing Analysis...")
        
        # Generate reports
        performance_report = logger.generate_performance_report()
        advanced_report = logger.generate_advanced_report()
        
        print(f"Health Score: {advanced_report['executive_summary']['health_score']:.1f}/100")
        print(f"Total Runtime: {advanced_report['executive_summary']['total_runtime']}")
        
        # Detect anomalies
        anomalies = logger.detect_anomalies()
        if anomalies:
            print("🚨 Anomalies Detected:")
            for anomaly in anomalies:
                print(f"  • {anomaly}")
        
        # Export data
        print("📤 Exporting Data...")
        json_file = logger.export_data("json", include_raw_data=True)
        csv_file = logger.export_data("csv")
        
        print(f"✅ JSON export: {json_file}")
        print(f"✅ CSV export: {csv_file}")
        
        # Create dashboard
        dashboard = logger.create_dashboard_html()
        print(f"🌐 Dashboard: {dashboard}")
        
        print("\n🔍 Final Analysis:")
        logger.view_insights(detailed=True)

if __name__ == "__main__":
    print("InsightLogger v1.5 - Comprehensive Examples")
    print("=" * 50)
    print()
    
    try:
        # Run all examples
        basic_logging_example()
        emoji_example()
        advanced_features_example()
        decorator_examples()
        export_and_analysis_example()
        
        print("All examples completed successfully!")
        print("\nCheck the '.insight' directory for generated files:")
        print("  • Log files and databases")
        print("  • Generated charts and graphs")
        print("  • HTML dashboards")
        print("  • Exported data files")
        
    except KeyboardInterrupt:
        print("\nExamples interrupted by user")
    except Exception as e:
        print(f"\nError in examples: {e}")
        import traceback
        traceback.print_exc()
