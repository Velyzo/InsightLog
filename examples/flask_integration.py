"""
InsightLogger v1.4 - Flask Web Application Integration Example

This example demonstrates how to integrate InsightLogger with a Flask web application
for comprehensive monitoring, logging, and analytics.
"""

from flask import Flask, request, jsonify, g
import time
import random
import traceback
from functools import wraps
from insightlog import InsightLogger

# Initialize Flask app
app = Flask(__name__)

# Initialize InsightLogger with enhanced features
logger = InsightLogger(
    name="FlaskApp",
    enable_database=True,
    enable_monitoring=True,
    enable_alerts=False,  # Set to True with email config for production
    log_level=20  # INFO level
)

# Custom decorator for API monitoring
def monitor_api(endpoint_name=None):
    """Decorator to monitor API endpoints"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.perf_counter()
            endpoint = endpoint_name or request.endpoint or f.__name__
            
            # Log request start
            logger.log_with_context(
                "INFO",
                f"API request started: {request.method} {request.path}",
                context={
                    "endpoint": endpoint,
                    "method": request.method,
                    "ip_address": request.remote_addr,
                    "user_agent": request.headers.get('User-Agent', 'Unknown')
                },
                tags=["api", "request", "start"]
            )
            
            try:
                # Execute the actual function
                with logger.performance_profile(f"api_{endpoint}"):
                    result = f(*args, **kwargs)
                
                # Calculate response time
                response_time = (time.perf_counter() - start_time) * 1000
                
                # Determine status code
                if isinstance(result, tuple):
                    status_code = result[1] if len(result) > 1 else 200
                else:
                    status_code = 200
                
                # Log successful request
                logger.track_api_call(request.path, request.method, response_time, status_code)
                logger.log_types("SUCCESS", f"API request completed: {endpoint} ({response_time:.1f}ms)")
                
                # Add custom metrics
                logger.add_custom_metric("api_response_time", response_time)
                logger.add_custom_metric("api_requests_total", 1)
                
                return result
                
            except Exception as e:
                # Calculate response time for errors too
                response_time = (time.perf_counter() - start_time) * 1000
                
                # Log error
                logger.log_types("ERROR", f"API request failed: {endpoint} - {str(e)}")
                logger.track_api_call(request.path, request.method, response_time, 500)
                
                # Log security event for certain errors
                if "unauthorized" in str(e).lower() or "forbidden" in str(e).lower():
                    logger.log_security_event(
                        "UNAUTHORIZED_ACCESS",
                        "MEDIUM",
                        f"Unauthorized access attempt to {endpoint} from {request.remote_addr}"
                    )
                
                # Add error metrics
                logger.add_custom_metric("api_errors_total", 1)
                
                raise
                
        return decorated_function
    return decorator

# Middleware for request logging
@app.before_request
def before_request():
    """Log all incoming requests"""
    g.start_time = time.perf_counter()
    
    # Log request details
    logger.log_with_context(
        "DEBUG",
        f"Incoming request: {request.method} {request.path}",
        context={
            "ip": request.remote_addr,
            "user_agent": request.headers.get('User-Agent'),
            "content_type": request.content_type,
            "content_length": request.content_length
        },
        tags=["request", "incoming"]
    )

@app.after_request
def after_request(response):
    """Log response details"""
    if hasattr(g, 'start_time'):
        response_time = (time.perf_counter() - g.start_time) * 1000
        
        logger.log_with_context(
            "DEBUG",
            f"Response sent: {response.status_code} ({response_time:.1f}ms)",
            context={
                "status_code": response.status_code,
                "response_time_ms": response_time,
                "content_type": response.content_type
            },
            tags=["response", "completed"]
        )
    
    return response

# API Routes

@app.route('/api/health')
@monitor_api('health_check')
def health_check():
    """Health check endpoint with comprehensive monitoring"""
    
    # Simulate health check operations
    with logger.performance_profile("health_check_database"):
        time.sleep(random.uniform(0.01, 0.05))  # Simulate DB check
        db_healthy = random.random() > 0.05  # 95% chance of being healthy
    
    with logger.performance_profile("health_check_external_services"):
        time.sleep(random.uniform(0.02, 0.08))  # Simulate external service check
        services_healthy = random.random() > 0.1  # 90% chance of being healthy
    
    # Calculate overall health
    health_score = logger._calculate_health_score()
    
    health_status = {
        "status": "healthy" if db_healthy and services_healthy and health_score > 70 else "unhealthy",
        "health_score": health_score,
        "database": "healthy" if db_healthy else "unhealthy",
        "external_services": "healthy" if services_healthy else "unhealthy",
        "timestamp": time.time()
    }
    
    # Log health check result
    if health_status["status"] == "healthy":
        logger.log_types("SUCCESS", f"Health check passed (score: {health_score:.1f})")
    else:
        logger.log_types("WARNING", f"Health check failed (score: {health_score:.1f})")
        logger.log_security_event("HEALTH_CHECK_FAILURE", "MEDIUM", "Health check failed")
    
    # Add health metrics
    logger.add_custom_metric("health_score", health_score)
    logger.add_custom_metric("health_check_duration", 
                           (time.perf_counter() - g.start_time) * 1000)
    
    status_code = 200 if health_status["status"] == "healthy" else 503
    return jsonify(health_status), status_code

@app.route('/api/users')
@monitor_api('get_users')
def get_users():
    """Get users endpoint with performance monitoring"""
    
    # Simulate database query
    @logger.log_function_time
    def query_users():
        time.sleep(random.uniform(0.1, 0.5))  # Simulate DB query time
        return [{"id": i, "name": f"User {i}"} for i in range(1, 11)]
    
    try:
        users = query_users()
        
        # Add metrics
        logger.add_custom_metric("users_queried", len(users))
        logger.add_custom_metric("database_queries", 1)
        
        logger.log_types("SUCCESS", f"Retrieved {len(users)} users")
        
        return jsonify({
            "users": users,
            "count": len(users),
            "timestamp": time.time()
        })
        
    except Exception as e:
        logger.log_types("ERROR", f"Failed to retrieve users: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/data', methods=['POST'])
@monitor_api('create_data')
def create_data():
    """Create data endpoint with validation and monitoring"""
    
    try:
        data = request.get_json()
        
        if not data:
            logger.log_types("WARNING", "Invalid request: No JSON data provided")
            logger.log_security_event("INVALID_REQUEST", "LOW", "Request with no JSON data")
            return jsonify({"error": "No data provided"}), 400
        
        # Simulate data processing
        with logger.performance_profile("data_validation"):
            time.sleep(random.uniform(0.05, 0.15))  # Simulate validation
            
        with logger.performance_profile("data_storage"):
            time.sleep(random.uniform(0.1, 0.3))  # Simulate storage
        
        # Log successful creation
        logger.log_with_context(
            "SUCCESS",
            "Data created successfully",
            context={
                "data_size": len(str(data)),
                "fields": list(data.keys()) if isinstance(data, dict) else "unknown"
            },
            tags=["data", "creation", "success"]
        )
        
        # Add metrics
        logger.add_custom_metric("data_created", 1)
        logger.add_custom_metric("data_size_bytes", len(str(data)))
        
        return jsonify({
            "message": "Data created successfully",
            "id": random.randint(1000, 9999),
            "timestamp": time.time()
        }), 201
        
    except Exception as e:
        logger.log_types("ERROR", f"Failed to create data: {str(e)}")
        logger.add_custom_metric("data_creation_errors", 1)
        return jsonify({"error": "Failed to create data"}), 500

@app.route('/api/login', methods=['POST'])
@monitor_api('user_login')
def login():
    """Login endpoint with security monitoring"""
    
    try:
        credentials = request.get_json()
        username = credentials.get('username') if credentials else None
        password = credentials.get('password') if credentials else None
        
        if not username or not password:
            logger.log_security_event(
                "LOGIN_ATTEMPT_INVALID",
                "LOW",
                f"Invalid login attempt from {request.remote_addr}"
            )
            return jsonify({"error": "Username and password required"}), 400
        
        # Simulate authentication
        with logger.performance_profile("authentication"):
            time.sleep(random.uniform(0.1, 0.3))  # Simulate auth check
            success = random.random() > 0.3  # 70% success rate
        
        if success:
            logger.log_security_event(
                "LOGIN_SUCCESS",
                "LOW",
                f"Successful login for user {username} from {request.remote_addr}"
            )
            logger.log_types("SUCCESS", f"User {username} logged in successfully")
            logger.add_custom_metric("successful_logins", 1)
            
            return jsonify({
                "message": "Login successful",
                "token": f"token_{random.randint(10000, 99999)}",
                "user": username
            })
        else:
            logger.log_security_event(
                "LOGIN_FAILURE",
                "MEDIUM",
                f"Failed login attempt for user {username} from {request.remote_addr}"
            )
            logger.log_types("WARNING", f"Failed login attempt for user {username}")
            logger.add_custom_metric("failed_logins", 1)
            
            return jsonify({"error": "Invalid credentials"}), 401
            
    except Exception as e:
        logger.log_types("ERROR", f"Login error: {str(e)}")
        logger.log_security_event("LOGIN_ERROR", "HIGH", f"Login system error: {str(e)}")
        return jsonify({"error": "Login system error"}), 500

@app.route('/api/report')
@monitor_api('generate_report')
def generate_report():
    """Generate report endpoint with heavy processing simulation"""
    
    @logger.log_function_time
    def process_report():
        """Simulate heavy report processing"""
        
        with logger.performance_profile("data_collection"):
            time.sleep(random.uniform(0.5, 1.5))  # Simulate data collection
            
        with logger.performance_profile("data_analysis"):
            time.sleep(random.uniform(1.0, 2.0))  # Simulate analysis
            
        with logger.performance_profile("report_generation"):
            time.sleep(random.uniform(0.3, 0.8))  # Simulate report generation
        
        return {
            "report_id": random.randint(1000, 9999),
            "data_points": random.randint(1000, 10000),
            "processing_time": time.perf_counter()
        }
    
    try:
        report = process_report()
        
        logger.log_types("SUCCESS", f"Report generated: ID {report['report_id']}")
        logger.add_custom_metric("reports_generated", 1)
        logger.add_custom_metric("report_data_points", report['data_points'])
        
        return jsonify({
            "report": report,
            "timestamp": time.time()
        })
        
    except Exception as e:
        logger.log_types("ERROR", f"Report generation failed: {str(e)}")
        return jsonify({"error": "Report generation failed"}), 500

@app.route('/admin/insights')
def admin_insights():
    """Admin endpoint to view insights"""
    
    try:
        # Check if this is an admin request (simple simulation)
        auth_header = request.headers.get('Authorization')
        if not auth_header or auth_header != "Bearer admin_token":
            logger.log_security_event(
                "UNAUTHORIZED_ADMIN_ACCESS",
                "HIGH",
                f"Unauthorized admin access attempt from {request.remote_addr}"
            )
            return jsonify({"error": "Unauthorized"}), 401
        
        logger.log_security_event(
            "ADMIN_ACCESS",
            "LOW",
            f"Admin accessed insights from {request.remote_addr}"
        )
        
        # Generate insights data
        performance_report = logger.generate_performance_report()
        advanced_report = logger.generate_advanced_report()
        anomalies = logger.detect_anomalies()
        
        insights_data = {
            "health_score": advanced_report['executive_summary']['health_score'],
            "total_runtime": str(advanced_report['executive_summary']['total_runtime']),
            "total_logs": advanced_report['executive_summary']['total_logs'],
            "system_metrics": performance_report['system_metrics'],
            "anomalies": anomalies,
            "security_events": len(logger.security_events),
            "function_performance": performance_report['function_performance']
        }
        
        logger.log_types("SUCCESS", "Admin insights accessed")
        return jsonify(insights_data)
        
    except Exception as e:
        logger.log_types("ERROR", f"Failed to generate insights: {str(e)}")
        return jsonify({"error": "Failed to generate insights"}), 500

# Error handlers

@app.errorhandler(404)
def not_found(error):
    logger.log_types("WARNING", f"404 error: {request.path} not found")
    logger.log_security_event("NOT_FOUND", "LOW", f"404 attempt: {request.path}")
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.log_types("ERROR", f"500 error: {str(error)}")
    logger.log_security_event("SERVER_ERROR", "HIGH", f"Internal server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.log_types("CRITICAL", f"Unhandled exception: {str(e)}")
    logger.log_with_context(
        "CRITICAL",
        "Unhandled exception occurred",
        context={
            "exception_type": type(e).__name__,
            "exception_message": str(e),
            "traceback": traceback.format_exc()
        },
        tags=["exception", "unhandled", "critical"]
    )
    return jsonify({"error": "An unexpected error occurred"}), 500

# Background task simulation
def simulate_background_tasks():
    """Simulate background tasks that generate metrics"""
    import threading
    import time
    
    def background_worker():
        while True:
            try:
                # Simulate various background operations
                logger.add_custom_metric("background_tasks_completed", 1)
                logger.add_custom_metric("queue_size", random.randint(0, 50))
                logger.add_custom_metric("active_connections", random.randint(10, 100))
                
                # Occasionally log background events
                if random.random() < 0.1:  # 10% chance
                    logger.log_types("INFO", "Background task completed", emoji=True)
                
                time.sleep(30)  # Run every 30 seconds
                
            except Exception as e:
                logger.log_types("ERROR", f"Background task error: {str(e)}")
                time.sleep(60)  # Wait longer on error
    
    # Start background thread
    bg_thread = threading.Thread(target=background_worker, daemon=True)
    bg_thread.start()

if __name__ == '__main__':
    print("🚀 Starting Flask Application with InsightLogger v1.4")
    print("=" * 60)
    
    # Start background tasks
    simulate_background_tasks()
    
    # Log application startup
    logger.log_types("SUCCESS", "Flask application starting up", emoji=True, bold=True)
    logger.log_with_context(
        "INFO",
        "Application configuration loaded",
        context={
            "debug_mode": app.debug,
            "environment": "development",
            "monitoring_enabled": True
        },
        tags=["startup", "configuration"]
    )
    
    try:
        print("\n📡 Available endpoints:")
        print("  • GET  /api/health - Health check")
        print("  • GET  /api/users - Get users")
        print("  • POST /api/data - Create data")
        print("  • POST /api/login - User login")
        print("  • GET  /api/report - Generate report")
        print("  • GET  /admin/insights - Admin insights (requires Authorization: Bearer admin_token)")
        print("\n🔍 Monitoring features:")
        print("  • Real-time performance tracking")
        print("  • Security event monitoring")
        print("  • Custom metrics collection")
        print("  • Automatic anomaly detection")
        print("  • Database logging enabled")
        print("\n🌐 Starting server on http://localhost:5000")
        print("💡 Use Ctrl+C to stop and view comprehensive insights")
        
        # Run the Flask app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Flask application...")
        logger.log_types("INFO", "Application shutdown initiated", emoji=True)
        
        # Generate final insights
        print("\n🔍 Generating final insights...")
        logger.view_insights(detailed=True, create_dashboard=True, export_format="json")
        
        # Export data
        export_file = logger.export_data("json", include_raw_data=True)
        print(f"📤 Application data exported to: {export_file}")
        
        logger.log_types("SUCCESS", "Application shutdown completed", emoji=True, bold=True)
        logger.stop_monitoring()
        
        print("\n✅ Flask application with InsightLogger demo completed!")
        print("Check the '.insight' directory for:")
        print("  • Detailed logs and analytics")
        print("  • Performance charts and graphs")
        print("  • Interactive HTML dashboard") 
        print("  • SQLite database with all metrics")
    
    except Exception as e:
        logger.log_types("CRITICAL", f"Application startup failed: {str(e)}")
        logger.stop_monitoring()
        raise
