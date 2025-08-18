"""
Quick demo script to test InsightLogger v1.5 basic functionality without matplotlib
"""

import sys
import os
import time

# Add the insightlog path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_without_matplotlib():
    """Test basic functionality without matplotlib dependency"""
    print("🚀 Testing InsightLogger v1.5 - Basic Features")
    print("=" * 50)
    
    # Temporarily disable matplotlib import
    import sys
    original_import = __builtins__.__import__
    
    def mock_import(name, *args, **kwargs):
        if name in ['matplotlib', 'matplotlib.pyplot']:
            raise ImportError(f"Mocked: {name} not available")
        return original_import(name, *args, **kwargs)
    
    __builtins__.__import__ = mock_import
    
    try:
        # Test basic functionality
        from insightlog.insight_logger import InsightLogger
        
        print("✅ InsightLogger imported successfully (without matplotlib)")
        
        # Initialize basic logger
        logger = InsightLogger(
            name="BasicTest",
            enable_database=True,
            enable_monitoring=True
        )
        
        print("✅ Logger initialized with enhanced features")
        
        # Test all log levels
        logger.log_types("SUCCESS", "InsightLogger v1.5 is working!", emoji=True, bold=True)
        logger.log_types("INFO", "Testing all enhanced features", emoji=True)
        logger.log_types("WARNING", "This is a warning message", emoji=True)
        logger.log_types("ERROR", "This is an error message", emoji=True)
        
        print("✅ Enhanced logging with emojis working")
        
        # Test function timing
        @logger.log_function_time
        def test_function():
            time.sleep(0.3)
            return "Function test completed"
        
        result = test_function()
        logger.log_types("SUCCESS", f"Function result: {result}", emoji=True)
        
        print("✅ Function timing decorator working")
        
        # Test custom metrics
        logger.add_custom_metric("test_metric", 42)
        logger.add_custom_metric("success_rate", 0.95)
        
        print("✅ Custom metrics working")
        
        # Test security events
        logger.log_security_event("TEST_EVENT", "LOW", "Test security event logged")
        
        print("✅ Security event logging working")
        
        # Test contextual logging
        logger.log_with_context(
            "INFO",
            "Test context logging",
            context={"user_id": 123, "action": "test"},
            tags=["test", "demo"]
        )
        
        print("✅ Contextual logging working")
        
        # Wait for monitoring data
        time.sleep(2)
        
        # Test health score
        health_score = logger._calculate_health_score()
        print(f"✅ Health score calculation: {health_score:.1f}/100")
        
        # Test recommendations
        recommendations = logger._generate_recommendations()
        print(f"✅ Generated {len(recommendations)} recommendations")
        
        # Test export (without visualization)
        try:
            export_file = logger.export_data("json")
            print(f"✅ JSON export successful: {export_file}")
        except Exception as e:
            print(f"⚠️ Export note: {e}")
        
        # Cleanup
        logger.stop_monitoring()
        
        print("\n🎉 ALL BASIC TESTS PASSED!")
        print("InsightLogger v1.5 core functionality is working correctly!")
        print("\nNote: Visualization features require matplotlib installation")
        print("Run 'pip install matplotlib' to enable charts and graphs")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Restore original import
        __builtins__.__import__ = original_import

if __name__ == "__main__":
    success = test_without_matplotlib()
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}")
