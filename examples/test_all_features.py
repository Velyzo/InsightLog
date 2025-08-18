#!/usr/bin/env python3
"""
InsightLogger v1.5 - Comprehensive Test Suite

This script tests all the new features and enhancements in InsightLogger v1.5
to ensure everything works correctly.
"""

import sys
import os
import time
import tempfile
import shutil
from pathlib import Path

# Add the insightlog module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from insightlog import InsightLogger, monitor_decorator, secure_log_decorator, MetricsCollector
    print("✅ InsightLogger module imported successfully")
except ImportError as e:
    print(f"❌ Failed to import InsightLogger: {e}")
    sys.exit(1)

def test_basic_functionality():
    """Test basic logging functionality"""
    print("\n🧪 Testing Basic Functionality")
    print("-" * 40)
    
    try:
        # Test basic initialization
        logger = InsightLogger(name="TestLogger", enable_database=False, enable_monitoring=False)
        print("✅ Basic initialization successful")
        
        # Test all log levels
        log_levels = ["INFO", "SUCCESS", "WARNING", "ERROR", "DEBUG", "TRACE", "HIGHLIGHT", "CRITICAL", "ALERT", "FAILURE"]
        for level in log_levels:
            logger.log_types(level, f"Test {level} message")
        print("✅ All log levels working")
        
        # Test enhanced formatting
        logger.log_types("INFO", "Test formatting", emoji=True, bold=True, border=True)
        print("✅ Enhanced formatting working")
        
        # Test function timing
        @logger.log_function_time
        def test_function():
            time.sleep(0.5)
            return "test result"
        
        result = test_function()
        assert result == "test result"
        print("✅ Function timing decorator working")
        
        logger.stop_monitoring()
        print("✅ Basic functionality tests passed")
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False
    
    return True

def test_enhanced_features():
    """Test enhanced features like database, monitoring, etc."""
    print("\n🧪 Testing Enhanced Features")
    print("-" * 40)
    
    try:
        # Test with all features enabled
        logger = InsightLogger(
            name="EnhancedTestLogger",
            enable_database=True,
            enable_monitoring=True,
            enable_alerts=False
        )
        print("✅ Enhanced initialization successful")
        
        # Test performance profiling
        with logger.performance_profile("test_operation"):
            time.sleep(0.2)
        print("✅ Performance profiling working")
        
        # Test custom metrics
        logger.add_custom_metric("test_metric", 42)
        logger.add_custom_metric("test_metric_2", 3.14)
        print("✅ Custom metrics working")
        
        # Test API tracking
        logger.track_api_call("/test/endpoint", "GET", 150, 200)
        print("✅ API tracking working")
        
        # Test security events
        logger.log_security_event("TEST_EVENT", "LOW", "Test security event")
        print("✅ Security event logging working")
        
        # Test contextual logging
        logger.log_with_context(
            "INFO",
            "Test context message",
            context={"user_id": 123, "action": "test"},
            tags=["test", "context"]
        )
        print("✅ Contextual logging working")
        
        # Test batch logging
        batch_logs = [
            {"level": "INFO", "message": "Batch message 1"},
            ("SUCCESS", "Batch message 2")
        ]
        logger.batch_log(batch_logs)
        print("✅ Batch logging working")
        
        # Wait for monitoring data
        time.sleep(2)
        
        # Test function statistics
        stats = logger.get_function_statistics()
        print("✅ Function statistics working")
        
        # Test anomaly detection
        anomalies = logger.detect_anomalies()
        print("✅ Anomaly detection working")
        
        # Test health score calculation
        health_score = logger._calculate_health_score()
        assert 0 <= health_score <= 100
        print("✅ Health score calculation working")
        
        # Test recommendations
        recommendations = logger._generate_recommendations()
        print("✅ Recommendations generation working")
        
        logger.stop_monitoring()
        print("✅ Enhanced features tests passed")
        
    except Exception as e:
        print(f"❌ Enhanced features test failed: {e}")
        return False
    
    return True

def test_export_and_visualization():
    """Test export and visualization features"""
    print("\n🧪 Testing Export and Visualization")
    print("-" * 40)
    
    try:
        with InsightLogger(
            name="ExportTestLogger",
            enable_database=True,
            enable_monitoring=True
        ) as logger:
            
            # Generate some data to export
            logger.log_types("INFO", "Test info message")
            logger.log_types("ERROR", "Test error message")
            logger.add_custom_metric("export_test_metric", 100)
            
            # Wait for some monitoring data
            time.sleep(1)
            
            # Test graph generation
            logger.draw_and_save_graph("log_frequency")
            print("✅ Graph generation working")
            
            # Test JSON export
            json_file = logger.export_data("json", include_raw_data=False)
            assert os.path.exists(json_file)
            print("✅ JSON export working")
            
            # Test CSV export
            csv_file = logger.export_data("csv")
            assert os.path.exists(csv_file)
            print("✅ CSV export working")
            
            # Test dashboard creation
            dashboard_file = logger.create_dashboard_html()
            assert os.path.exists(dashboard_file)
            print("✅ Dashboard creation working")
            
            # Test performance report
            perf_report = logger.generate_performance_report()
            assert isinstance(perf_report, dict)
            print("✅ Performance report generation working")
            
            # Test advanced report
            advanced_report = logger.generate_advanced_report()
            assert isinstance(advanced_report, dict)
            print("✅ Advanced report generation working")
            
        print("✅ Export and visualization tests passed")
        
    except Exception as e:
        print(f"❌ Export and visualization test failed: {e}")
        return False
    
    return True

def test_context_manager():
    """Test context manager functionality"""
    print("\n🧪 Testing Context Manager")
    print("-" * 40)
    
    try:
        # Test normal exit
        with InsightLogger(name="ContextTestLogger", enable_monitoring=True) as logger:
            logger.log_types("INFO", "Context manager test")
            logger.add_custom_metric("context_test", 1)
        print("✅ Normal context manager exit working")
        
        # Test exception handling
        try:
            with InsightLogger(name="ContextExceptionLogger", enable_monitoring=True) as logger:
                logger.log_types("INFO", "Before exception")
                raise ValueError("Test exception")
        except ValueError:
            pass  # Expected
        print("✅ Context manager exception handling working")
        
        print("✅ Context manager tests passed")
        
    except Exception as e:
        print(f"❌ Context manager test failed: {e}")
        return False
    
    return True

def test_decorators():
    """Test decorator functionality"""
    print("\n🧪 Testing Decorators")
    print("-" * 40)
    
    try:
        logger = InsightLogger(name="DecoratorTestLogger", enable_monitoring=True)
        
        # Test monitor decorator
        monitor_func = monitor_decorator(logger)
        
        @monitor_func
        def test_monitored_function():
            time.sleep(0.1)
            return "monitored result"
        
        result = test_monitored_function()
        assert result == "monitored result"
        print("✅ Monitor decorator working")
        
        # Test secure log decorator
        secure_func = secure_log_decorator(logger)
        
        @secure_func
        def test_secure_function(data):
            return f"processed {data}"
        
        result = test_secure_function("test data")
        assert "processed test data" in result
        print("✅ Secure log decorator working")
        
        # Test metrics collector
        metrics = MetricsCollector(logger)
        
        with metrics.time_operation("test_operation"):
            time.sleep(0.1)
        
        metrics.count_event("test_event")
        metrics.gauge_value("test_gauge", 50)
        print("✅ Metrics collector working")
        
        logger.stop_monitoring()
        print("✅ Decorator tests passed")
        
    except Exception as e:
        print(f"❌ Decorator test failed: {e}")
        return False
    
    return True

def test_database_functionality():
    """Test database-related functionality"""
    print("\n🧪 Testing Database Functionality")
    print("-" * 40)
    
    try:
        logger = InsightLogger(
            name="DatabaseTestLogger",
            enable_database=True,
            enable_monitoring=False
        )
        
        # Verify database was created
        assert hasattr(logger, 'conn')
        assert hasattr(logger, 'db_path')
        assert os.path.exists(logger.db_path)
        print("✅ Database creation working")
        
        # Test log filtering
        logger.log_types("INFO", "Test info for filtering")
        logger.log_types("ERROR", "Test error for filtering")
        
        # Test database queries
        filtered_logs = logger.create_log_filter(level="INFO")
        print("✅ Database filtering working")
        
        logger.stop_monitoring()
        print("✅ Database functionality tests passed")
        
    except Exception as e:
        print(f"❌ Database functionality test failed: {e}")
        return False
    
    return True

def test_error_handling():
    """Test error handling and edge cases"""
    print("\n🧪 Testing Error Handling")
    print("-" * 40)
    
    try:
        # Test with invalid parameters
        logger = InsightLogger(
            name="ErrorTestLogger",
            enable_database=True,
            enable_monitoring=True,
            enable_alerts=False  # No email config
        )
        
        # Test function with errors
        @logger.log_function_time
        def error_function():
            raise ValueError("Test error")
        
        try:
            error_function()
        except ValueError:
            pass  # Expected
        print("✅ Function error handling working")
        
        # Test invalid log level
        logger.log_types("INVALID_LEVEL", "This should still work")
        print("✅ Invalid log level handling working")
        
        # Test empty batch logging
        logger.batch_log([])
        print("✅ Empty batch logging handling working")
        
        # Test with None values
        logger.add_custom_metric("none_test", None)
        print("✅ None value handling working")
        
        logger.stop_monitoring()
        print("✅ Error handling tests passed")
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False
    
    return True

def test_performance():
    """Test performance and memory usage"""
    print("\n🧪 Testing Performance")
    print("-" * 40)
    
    try:
        import psutil
        import gc
        
        # Measure initial memory
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        logger = InsightLogger(
            name="PerformanceTestLogger",
            enable_database=True,
            enable_monitoring=True
        )
        
        # Generate many log entries
        start_time = time.perf_counter()
        for i in range(1000):
            logger.log_types("INFO", f"Performance test message {i}")
            if i % 100 == 0:
                logger.add_custom_metric(f"test_metric_{i}", i)
        
        end_time = time.perf_counter()
        log_time = end_time - start_time
        
        # Measure memory usage
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"✅ Performance test completed:")
        print(f"  • 1000 log entries in {log_time:.2f} seconds")
        print(f"  • {log_time*1000:.2f} ms per 1000 entries")
        print(f"  • Memory increase: {memory_increase:.2f} MB")
        
        # Performance should be reasonable
        assert log_time < 10.0  # Should complete in under 10 seconds
        assert memory_increase < 100  # Should not use more than 100MB
        
        logger.stop_monitoring()
        
        # Force garbage collection
        gc.collect()
        
        print("✅ Performance tests passed")
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False
    
    return True

def cleanup_test_files():
    """Clean up test files"""
    print("\n🧹 Cleaning up test files...")
    
    try:
        insight_dir = Path(".insight")
        if insight_dir.exists():
            # Remove test files but keep structure
            for file_path in insight_dir.glob("*test*"):
                if file_path.is_file():
                    file_path.unlink()
                    
        print("✅ Test files cleaned up")
        
    except Exception as e:
        print(f"⚠️ Cleanup warning: {e}")

def run_all_tests():
    """Run all test suites"""
    print("🧪 InsightLogger v1.5 - Comprehensive Test Suite")
    print("=" * 60)
    
    tests = [
        test_basic_functionality,
        test_enhanced_features,
        test_export_and_visualization,
        test_context_manager,
        test_decorators,
        test_database_functionality,
        test_error_handling,
        test_performance
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test_func.__name__} crashed: {e}")
            failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("🏁 Test Suite Summary")
    print("=" * 60)
    print(f"✅ Tests Passed: {passed}")
    print(f"❌ Tests Failed: {failed}")
    print(f"📊 Success Rate: {(passed/(passed+failed))*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 All tests passed! InsightLogger v1.5 is working correctly!")
    else:
        print(f"\n⚠️ {failed} test(s) failed. Please check the output above for details.")
    
    # Cleanup
    cleanup_test_files()
    
    return failed == 0

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
        cleanup_test_files()
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 Test suite crashed: {e}")
        import traceback
        traceback.print_exc()
        cleanup_test_files()
        sys.exit(1)
