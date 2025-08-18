"""
InsightLogger Comprehensive Tkinter Demo Application

This application provides a complete graphical interface to test every single function
and feature of the InsightLogger library. It includes buttons, forms, and displays
for comprehensive testing of all capabilities.

Author: Velyzo
Version: 1.5.0 Demo
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog
import threading
import time
import random
import json
import os
import sys
from datetime import datetime
import webbrowser

# Add the insightlog module to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from insightlog import InsightLogger
except ImportError:
    from insightlog.insight_logger import InsightLogger

class InsightLoggerDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("InsightLogger v1.5 - Comprehensive Testing Suite")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize logger
        self.logger = None
        self.demo_thread = None
        self.monitoring_active = False
        
        # Create the GUI
        self.create_widgets()
        
        # Initialize with default logger
        self.initialize_logger()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Create main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="InsightLogger v1.5 - Complete Testing Suite", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Left panel for controls
        left_panel = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        left_panel.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Right panel for output
        right_panel = ttk.LabelFrame(main_frame, text="Output & Results", padding="10")
        right_panel.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create control sections
        self.create_logger_config_section(left_panel)
        self.create_basic_logging_section(left_panel)
        self.create_advanced_features_section(left_panel)
        self.create_monitoring_section(left_panel)
        self.create_analytics_section(left_panel)
        self.create_export_section(left_panel)
        
        # Create output section
        self.create_output_section(right_panel)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Initialize logger to start testing")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_logger_config_section(self, parent):
        """Create logger configuration section"""
        config_frame = ttk.LabelFrame(parent, text="Logger Configuration", padding="5")
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Logger name
        ttk.Label(config_frame, text="Logger Name:").grid(row=0, column=0, sticky=tk.W)
        self.logger_name_var = tk.StringVar(value="DemoLogger")
        ttk.Entry(config_frame, textvariable=self.logger_name_var, width=20).grid(row=0, column=1, sticky=tk.W)
        
        # Configuration options
        self.enable_database_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(config_frame, text="Enable Database", variable=self.enable_database_var).grid(row=1, column=0, columnspan=2, sticky=tk.W)
        
        self.enable_monitoring_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(config_frame, text="Enable Monitoring", variable=self.enable_monitoring_var).grid(row=2, column=0, columnspan=2, sticky=tk.W)
        
        self.enable_alerts_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(config_frame, text="Enable Alerts", variable=self.enable_alerts_var).grid(row=3, column=0, columnspan=2, sticky=tk.W)
        
        # Initialize/Reinitialize button
        ttk.Button(config_frame, text="Initialize Logger", command=self.initialize_logger).grid(row=4, column=0, columnspan=2, pady=5)
    
    def create_basic_logging_section(self, parent):
        """Create basic logging test section"""
        basic_frame = ttk.LabelFrame(parent, text="Basic Logging Tests", padding="5")
        basic_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Log levels
        log_levels = ["INFO", "DEBUG", "ERROR", "SUCCESS", "FAILURE", "WARNING", "ALERT", "TRACE", "HIGHLIGHT", "CRITICAL"]
        
        for i, level in enumerate(log_levels):
            row = i // 2
            col = i % 2
            ttk.Button(basic_frame, text=f"Log {level}", 
                      command=lambda l=level: self.test_log_level(l)).grid(row=row, column=col, padx=2, pady=2, sticky=tk.W+tk.E)
        
        # Custom message logging
        ttk.Label(basic_frame, text="Custom Message:").grid(row=len(log_levels)//2 + 1, column=0, sticky=tk.W)
        self.custom_message_var = tk.StringVar(value="Custom test message")
        ttk.Entry(basic_frame, textvariable=self.custom_message_var, width=30).grid(row=len(log_levels)//2 + 1, column=1, sticky=tk.W+tk.E)
        
        ttk.Button(basic_frame, text="Log Custom Message", command=self.test_custom_message).grid(row=len(log_levels)//2 + 2, column=0, columnspan=2, pady=5)
    
    def create_advanced_features_section(self, parent):
        """Create advanced features test section"""
        advanced_frame = ttk.LabelFrame(parent, text="Advanced Features", padding="5")
        advanced_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Context logging
        ttk.Button(advanced_frame, text="Test Context Logging", command=self.test_context_logging).grid(row=0, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        # Batch logging
        ttk.Button(advanced_frame, text="Test Batch Logging", command=self.test_batch_logging).grid(row=1, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        # Function timing
        ttk.Button(advanced_frame, text="Test Function Timing", command=self.test_function_timing).grid(row=2, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        # Performance profiling
        ttk.Button(advanced_frame, text="Test Performance Profiling", command=self.test_performance_profiling).grid(row=3, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        # Security events
        ttk.Button(advanced_frame, text="Test Security Events", command=self.test_security_events).grid(row=4, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        # Custom metrics
        ttk.Button(advanced_frame, text="Test Custom Metrics", command=self.test_custom_metrics).grid(row=5, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        # API monitoring
        ttk.Button(advanced_frame, text="Test API Monitoring", command=self.test_api_monitoring).grid(row=6, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
    
    def create_monitoring_section(self, parent):
        """Create monitoring test section"""
        monitoring_frame = ttk.LabelFrame(parent, text="System Monitoring", padding="5")
        monitoring_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Start/Stop monitoring
        self.monitoring_button = ttk.Button(monitoring_frame, text="Start Monitoring", command=self.toggle_monitoring)
        self.monitoring_button.grid(row=0, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        # Memory stress test
        ttk.Button(monitoring_frame, text="Memory Stress Test", command=self.test_memory_stress).grid(row=1, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        # CPU stress test
        ttk.Button(monitoring_frame, text="CPU Stress Test", command=self.test_cpu_stress).grid(row=2, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        # Network monitoring
        ttk.Button(monitoring_frame, text="Test Network Monitoring", command=self.test_network_monitoring).grid(row=3, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
    
    def create_analytics_section(self, parent):
        """Create analytics and visualization section"""
        analytics_frame = ttk.LabelFrame(parent, text="Analytics & Visualization", padding="5")
        analytics_frame.pack(fill=tk.X, pady=(0, 10))
        
        # View insights
        ttk.Button(analytics_frame, text="View Basic Insights", command=self.view_basic_insights).grid(row=0, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        ttk.Button(analytics_frame, text="View Detailed Insights", command=self.view_detailed_insights).grid(row=1, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        # Generate visualizations
        ttk.Button(analytics_frame, text="Generate All Graphs", command=self.generate_all_graphs).grid(row=2, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        ttk.Button(analytics_frame, text="Generate Performance Graph", command=lambda: self.generate_specific_graph("performance")).grid(row=3, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        ttk.Button(analytics_frame, text="Generate Error Graph", command=lambda: self.generate_specific_graph("errors")).grid(row=4, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        # Dashboard
        ttk.Button(analytics_frame, text="Create HTML Dashboard", command=self.create_dashboard).grid(row=5, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        # Recommendations
        ttk.Button(analytics_frame, text="Get AI Recommendations", command=self.get_recommendations).grid(row=6, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
    
    def create_export_section(self, parent):
        """Create export and utility section"""
        export_frame = ttk.LabelFrame(parent, text="Export & Utilities", padding="5")
        export_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Export data
        ttk.Button(export_frame, text="Export to JSON", command=lambda: self.export_data("json")).grid(row=0, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        ttk.Button(export_frame, text="Export to CSV", command=lambda: self.export_data("csv")).grid(row=1, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        # Advanced reports
        ttk.Button(export_frame, text="Generate Advanced Report", command=self.generate_advanced_report).grid(row=2, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        # Function statistics
        ttk.Button(export_frame, text="Get Function Statistics", command=self.get_function_statistics).grid(row=3, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        # Health check
        ttk.Button(export_frame, text="Calculate Health Score", command=self.calculate_health_score).grid(row=4, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        # Clear data
        ttk.Button(export_frame, text="Clear All Data", command=self.clear_all_data).grid(row=5, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
        
        # Open insight folder
        ttk.Button(export_frame, text="Open Insight Folder", command=self.open_insight_folder).grid(row=6, column=0, columnspan=2, pady=2, sticky=tk.W+tk.E)
    
    def create_output_section(self, parent):
        """Create output display section"""
        # Output text area
        self.output_text = scrolledtext.ScrolledText(parent, width=80, height=35, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Buttons for output control
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Clear Output", command=self.clear_output).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Save Output", command=self.save_output).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Auto-scroll", command=self.toggle_autoscroll).pack(side=tk.LEFT)
        
        self.autoscroll = True
    
    def log_to_output(self, message):
        """Add message to output display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\\n"
        
        self.output_text.insert(tk.END, formatted_message)
        if self.autoscroll:
            self.output_text.see(tk.END)
        
        # Also update status
        self.status_var.set(f"Last action: {message[:50]}...")
    
    def initialize_logger(self):
        """Initialize or reinitialize the logger"""
        try:
            if self.logger:
                # Stop existing monitoring
                if hasattr(self.logger, 'stop_monitoring'):
                    self.logger.stop_monitoring()
            
            # Create new logger instance
            self.logger = InsightLogger(
                name=self.logger_name_var.get(),
                enable_database=self.enable_database_var.get(),
                enable_monitoring=self.enable_monitoring_var.get(),
                enable_alerts=self.enable_alerts_var.get()
            )
            
            self.log_to_output(f"Logger '{self.logger_name_var.get()}' initialized successfully")
            self.log_to_output(f"Database: {self.enable_database_var.get()}, Monitoring: {self.enable_monitoring_var.get()}, Alerts: {self.enable_alerts_var.get()}")
            
        except Exception as e:
            self.log_to_output(f"Error initializing logger: {str(e)}")
            messagebox.showerror("Error", f"Failed to initialize logger: {str(e)}")
    
    def test_log_level(self, level):
        """Test logging at specified level"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            test_messages = {
                "INFO": "This is an informational message",
                "DEBUG": "Debug information for troubleshooting",
                "ERROR": "An error occurred during processing", 
                "SUCCESS": "Operation completed successfully",
                "FAILURE": "Operation failed to complete",
                "WARNING": "Warning: potential issue detected",
                "ALERT": "Alert: immediate attention required",
                "TRACE": "Trace: detailed execution flow",
                "HIGHLIGHT": "Important: highlighted information",
                "CRITICAL": "Critical: system stability at risk"
            }
            
            message = test_messages.get(level, f"Test message for {level}")
            
            # Add some formatting variety
            formatting_options = {
                "emoji": random.choice([True, False]),
                "bold": random.choice([True, False]),
                "border": random.choice([True, False]),
                "urgent": level in ["ERROR", "CRITICAL", "ALERT"]
            }
            
            self.logger.log_types(level, message, **formatting_options)
            self.log_to_output(f"Logged {level}: {message}")
            
        except Exception as e:
            self.log_to_output(f"Error logging {level}: {str(e)}")
    
    def test_custom_message(self):
        """Test custom message logging"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            message = self.custom_message_var.get()
            level = "INFO"  # Default level for custom messages
            
            self.logger.log_types(level, message, emoji=True, bold=True)
            self.log_to_output(f"Custom message logged: {message}")
            
        except Exception as e:
            self.log_to_output(f"Error logging custom message: {str(e)}")
    
    def test_context_logging(self):
        """Test context logging with metadata"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            context = {
                "user_id": random.randint(1000, 9999),
                "session_id": f"sess_{random.randint(100, 999)}",
                "ip_address": f"192.168.1.{random.randint(1, 254)}",
                "user_agent": "DemoApp/1.0",
                "timestamp": datetime.now().isoformat()
            }
            
            tags = ["demo", "context_test", "gui_testing"]
            
            self.logger.log_with_context(
                "INFO",
                "Context logging demonstration with metadata",
                context=context,
                tags=tags
            )
            
            self.log_to_output(f"Context logging completed with {len(context)} metadata fields and {len(tags)} tags")
            
        except Exception as e:
            self.log_to_output(f"Error in context logging: {str(e)}")
    
    def test_batch_logging(self):
        """Test batch logging functionality"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            batch_logs = []
            
            # Create a batch of different log types
            for i in range(10):
                level = random.choice(["INFO", "DEBUG", "WARNING", "SUCCESS"])
                message = f"Batch log entry #{i+1} - {level} message"
                batch_logs.append({"level": level, "message": message})
            
            # Add some tuple format logs
            batch_logs.extend([
                ("ERROR", "Simulated error in batch processing"),
                ("SUCCESS", "Batch operation completed successfully"),
                ("INFO", "Final batch entry")
            ])
            
            self.logger.batch_log(batch_logs)
            self.log_to_output(f"Batch logging completed: {len(batch_logs)} entries processed")
            
        except Exception as e:
            self.log_to_output(f"Error in batch logging: {str(e)}")
    
    def test_function_timing(self):
        """Test function timing decorator"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            @self.logger.log_function_time
            def demo_function(duration=2, operation="data_processing"):
                """Demo function to test timing decorator"""
                time.sleep(duration)
                # Simulate some work
                result = sum(i * i for i in range(10000))
                return f"Operation '{operation}' completed with result: {result}"
            
            # Test the function
            result = demo_function(1.5, "demo_calculation")
            self.log_to_output(f"Function timing test completed: {result}")
            
        except Exception as e:
            self.log_to_output(f"Error in function timing test: {str(e)}")
    
    def test_performance_profiling(self):
        """Test performance profiling with context manager"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            with self.logger.performance_profile("gui_demo_profiling"):
                # Simulate various operations
                self.log_to_output("Starting performance profiling test...")
                
                # CPU intensive task
                result = sum(i ** 2 for i in range(50000))
                
                # Memory allocation
                large_list = list(range(100000))
                
                # String operations
                text_data = "demo " * 10000
                processed_text = text_data.upper().split()
                
                time.sleep(0.5)  # Simulate I/O wait
                
            self.log_to_output("Performance profiling completed successfully")
            
        except Exception as e:
            self.log_to_output(f"Error in performance profiling: {str(e)}")
    
    def test_security_events(self):
        """Test security event logging"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            security_events = [
                ("LOGIN_ATTEMPT", "LOW", "User login from GUI demo application"),
                ("DATA_ACCESS", "MEDIUM", "Sensitive data accessed during testing"),
                ("PERMISSION_CHANGE", "HIGH", "Security permissions modified"),
                ("SUSPICIOUS_ACTIVITY", "HIGH", "Multiple failed authentication attempts"),
                ("SYSTEM_CHANGE", "MEDIUM", "System configuration modified via GUI")
            ]
            
            for event_type, severity, description in security_events:
                self.logger.log_security_event(event_type, severity, description)
                time.sleep(0.1)  # Small delay for realistic timing
            
            self.log_to_output(f"Security event testing completed: {len(security_events)} events logged")
            
        except Exception as e:
            self.log_to_output(f"Error in security event testing: {str(e)}")
    
    def test_custom_metrics(self):
        """Test custom metrics functionality"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            # Simulate various application metrics
            metrics = {
                "gui_response_time": random.uniform(10, 100),
                "user_actions_per_minute": random.randint(5, 25),
                "memory_usage_mb": random.uniform(50, 200),
                "cpu_utilization": random.uniform(10, 80),
                "active_connections": random.randint(1, 10),
                "cache_hit_ratio": random.uniform(0.7, 0.99),
                "error_rate": random.uniform(0.01, 0.05),
                "throughput_ops_sec": random.uniform(100, 1000)
            }
            
            for metric_name, value in metrics.items():
                self.logger.add_custom_metric(metric_name, value)
            
            self.log_to_output(f"Custom metrics added: {len(metrics)} metrics with values")
            
            # Display some metrics
            for name, value in list(metrics.items())[:3]:
                self.log_to_output(f"  {name}: {value:.2f}")
            
        except Exception as e:
            self.log_to_output(f"Error in custom metrics test: {str(e)}")
    
    def test_api_monitoring(self):
        """Test API monitoring functionality"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            # Simulate API calls
            api_endpoints = [
                "/api/users",
                "/api/data/export", 
                "/api/auth/login",
                "/api/reports/generate",
                "/api/settings/update"
            ]
            
            for endpoint in api_endpoints:
                method = random.choice(["GET", "POST", "PUT", "DELETE"])
                response_time = random.uniform(50, 800)
                status_code = random.choice([200, 200, 200, 201, 400, 404, 500])  # Mostly success
                
                self.logger.track_api_call(endpoint, method, response_time, status_code)
                time.sleep(0.1)  # Simulate realistic timing
            
            self.log_to_output(f"API monitoring test completed: {len(api_endpoints)} API calls tracked")
            
        except Exception as e:
            self.log_to_output(f"Error in API monitoring test: {str(e)}")
    
    def toggle_monitoring(self):
        """Start or stop system monitoring"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            if not self.monitoring_active:
                # Start monitoring (it should already be started by default)
                self.monitoring_active = True
                self.monitoring_button.configure(text="Stop Monitoring")
                self.log_to_output("System monitoring started")
            else:
                # Stop monitoring
                if hasattr(self.logger, 'stop_monitoring'):
                    self.logger.stop_monitoring()
                self.monitoring_active = False
                self.monitoring_button.configure(text="Start Monitoring")
                self.log_to_output("System monitoring stopped")
                
        except Exception as e:
            self.log_to_output(f"Error toggling monitoring: {str(e)}")
    
    def test_memory_stress(self):
        """Test memory stress to trigger monitoring alerts"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        def memory_stress():
            try:
                self.log_to_output("Starting memory stress test...")
                
                # Allocate progressively more memory
                memory_consumers = []
                for i in range(5):
                    # Allocate 10MB chunks
                    chunk = [0] * (10 * 1024 * 1024 // 8)  # Divide by 8 for 64-bit integers
                    memory_consumers.append(chunk)
                    self.log_to_output(f"Allocated memory chunk {i+1}/5")
                    time.sleep(1)
                
                # Hold memory for a few seconds
                time.sleep(3)
                
                # Release memory
                memory_consumers.clear()
                self.log_to_output("Memory stress test completed - memory released")
                
            except Exception as e:
                self.log_to_output(f"Error in memory stress test: {str(e)}")
        
        # Run in separate thread to avoid blocking GUI
        threading.Thread(target=memory_stress, daemon=True).start()
    
    def test_cpu_stress(self):
        """Test CPU stress to trigger monitoring alerts"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        def cpu_stress():
            try:
                self.log_to_output("Starting CPU stress test...")
                
                # CPU intensive calculations
                start_time = time.time()
                while time.time() - start_time < 5:  # Run for 5 seconds
                    # Perform CPU intensive operations
                    result = sum(i ** 2 for i in range(10000))
                    
                self.log_to_output("CPU stress test completed")
                
            except Exception as e:
                self.log_to_output(f"Error in CPU stress test: {str(e)}")
        
        # Run in separate thread
        threading.Thread(target=cpu_stress, daemon=True).start()
    
    def test_network_monitoring(self):
        """Test network monitoring functionality"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            # Simulate network operations
            import urllib.request
            
            self.log_to_output("Testing network monitoring...")
            
            # Track some network "requests" (simulated)
            for i in range(5):
                bytes_sent = random.randint(100, 1000)
                bytes_received = random.randint(500, 5000)
                latency = random.uniform(10, 100)
                
                self.logger.track_network_stats("test_request", bytes_sent, bytes_received, latency)
                time.sleep(0.2)
            
            self.log_to_output("Network monitoring test completed")
            
        except Exception as e:
            self.log_to_output(f"Error in network monitoring test: {str(e)}")
    
    def view_basic_insights(self):
        """View basic insights"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            self.log_to_output("Generating basic insights...")
            self.logger.view_insights(detailed=False)
            self.log_to_output("Basic insights generated (check console output)")
            
        except Exception as e:
            self.log_to_output(f"Error viewing basic insights: {str(e)}")
    
    def view_detailed_insights(self):
        """View detailed insights"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            self.log_to_output("Generating detailed insights...")
            self.logger.view_insights(detailed=True)
            self.log_to_output("Detailed insights generated (check console output)")
            
        except Exception as e:
            self.log_to_output(f"Error viewing detailed insights: {str(e)}")
    
    def generate_all_graphs(self):
        """Generate all visualization graphs"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            self.log_to_output("Generating all graphs...")
            result = self.logger.draw_and_save_graph("all")
            self.log_to_output(f"All graphs generated: {result}")
            
        except Exception as e:
            self.log_to_output(f"Error generating graphs: {str(e)}")
    
    def generate_specific_graph(self, graph_type):
        """Generate specific type of graph"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            self.log_to_output(f"Generating {graph_type} graph...")
            result = self.logger.draw_and_save_graph(graph_type)
            self.log_to_output(f"{graph_type.capitalize()} graph generated: {result}")
            
        except Exception as e:
            self.log_to_output(f"Error generating {graph_type} graph: {str(e)}")
    
    def create_dashboard(self):
        """Create HTML dashboard"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            self.log_to_output("Creating HTML dashboard...")
            dashboard_path = self.logger.create_dashboard()
            self.log_to_output(f"Dashboard created: {dashboard_path}")
            
            # Ask if user wants to open dashboard
            if messagebox.askyesno("Dashboard Created", "Dashboard created successfully! Would you like to open it in your browser?"):
                webbrowser.open(f"file://{os.path.abspath(dashboard_path)}")
            
        except Exception as e:
            self.log_to_output(f"Error creating dashboard: {str(e)}")
    
    def get_recommendations(self):
        """Get AI recommendations"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            self.log_to_output("Generating AI recommendations...")
            recommendations = self.logger._generate_recommendations()
            
            self.log_to_output(f"Generated {len(recommendations)} recommendations:")
            for i, rec in enumerate(recommendations[:5], 1):  # Show first 5
                self.log_to_output(f"  {i}. {rec}")
            
            if len(recommendations) > 5:
                self.log_to_output(f"  ... and {len(recommendations) - 5} more recommendations")
                
        except Exception as e:
            self.log_to_output(f"Error getting recommendations: {str(e)}")
    
    def export_data(self, format_type):
        """Export data in specified format"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            self.log_to_output(f"Exporting data to {format_type.upper()}...")
            result = self.logger.export_data(format_type, include_raw_data=True)
            
            if isinstance(result, str) and os.path.exists(result):
                self.log_to_output(f"Data exported to: {result}")
                
                # Ask if user wants to open the file
                if messagebox.askyesno("Export Complete", f"Data exported to {format_type.upper()} successfully! Would you like to open the file?"):
                    if format_type == "json":
                        os.startfile(result)  # Windows specific
                    elif format_type == "csv":
                        os.startfile(result)  # Windows specific
            else:
                self.log_to_output(f"Export completed: {result}")
                
        except Exception as e:
            self.log_to_output(f"Error exporting to {format_type}: {str(e)}")
    
    def generate_advanced_report(self):
        """Generate advanced analytics report"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            self.log_to_output("Generating advanced report...")
            report = self.logger.generate_advanced_report()
            
            # Display key metrics from report
            exec_summary = report.get('executive_summary', {})
            self.log_to_output("Advanced Report Generated:")
            self.log_to_output(f"  Health Score: {exec_summary.get('health_score', 'N/A')}")
            self.log_to_output(f"  Total Runtime: {exec_summary.get('total_runtime', 'N/A')}")
            self.log_to_output(f"  Recommendations: {exec_summary.get('recommendation_count', 0)}")
            self.log_to_output(f"  Report sections: {len(report)} sections")
            
        except Exception as e:
            self.log_to_output(f"Error generating advanced report: {str(e)}")
    
    def get_function_statistics(self):
        """Get function execution statistics"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            stats = self.logger.get_function_statistics()
            
            if stats:
                self.log_to_output(f"Function Statistics ({len(stats)} functions):")
                # Sort by average execution time
                sorted_stats = sorted(stats.items(), key=lambda x: x[1].get('avg_time', 0), reverse=True)
                
                for func_name, func_stats in sorted_stats[:5]:  # Show top 5
                    avg_time = func_stats.get('avg_time', 0)
                    call_count = func_stats.get('call_count', 0)
                    self.log_to_output(f"  {func_name}: {avg_time:.1f}ms avg, {call_count} calls")
            else:
                self.log_to_output("No function statistics available yet")
                
        except Exception as e:
            self.log_to_output(f"Error getting function statistics: {str(e)}")
    
    def calculate_health_score(self):
        """Calculate and display system health score"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            health_score = self.logger.calculate_health_score()
            
            self.log_to_output(f"System Health Score: {health_score:.1f}/100")
            
            if health_score >= 80:
                self.log_to_output("  Status: Excellent health")
            elif health_score >= 60:
                self.log_to_output("  Status: Good health")
            elif health_score >= 40:
                self.log_to_output("  Status: Fair health - attention needed")
            else:
                self.log_to_output("  Status: Poor health - immediate action required")
                
        except Exception as e:
            self.log_to_output(f"Error calculating health score: {str(e)}")
    
    def clear_all_data(self):
        """Clear all logger data"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all logger data? This action cannot be undone."):
            try:
                # Clear various data structures
                self.logger.error_count.clear()
                self.logger.execution_times.clear()
                self.logger.function_error_count.clear()
                self.logger.memory_usage.clear()
                self.logger.cpu_usage.clear()
                self.logger.network_stats.clear()
                self.logger.custom_metrics.clear()
                self.logger.security_events.clear()
                self.logger.api_calls.clear()
                
                self.log_to_output("All logger data cleared successfully")
                
            except Exception as e:
                self.log_to_output(f"Error clearing data: {str(e)}")
    
    def open_insight_folder(self):
        """Open the insight folder in file explorer"""
        if not self.logger:
            messagebox.showwarning("Warning", "Please initialize logger first")
            return
        
        try:
            insight_path = self.logger.insight_dir
            if os.path.exists(insight_path):
                os.startfile(insight_path)  # Windows specific
                self.log_to_output(f"Opened insight folder: {insight_path}")
            else:
                self.log_to_output("Insight folder does not exist yet")
                
        except Exception as e:
            self.log_to_output(f"Error opening insight folder: {str(e)}")
    
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete(1.0, tk.END)
    
    def save_output(self):
        """Save output to file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.output_text.get(1.0, tk.END))
                self.log_to_output(f"Output saved to: {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save output: {str(e)}")
    
    def toggle_autoscroll(self):
        """Toggle auto-scroll functionality"""
        self.autoscroll = not self.autoscroll
        status = "enabled" if self.autoscroll else "disabled"
        self.log_to_output(f"Auto-scroll {status}")

def main():
    """Main function to run the demo application"""
    root = tk.Tk()
    app = InsightLoggerDemo(root)
    
    # Handle window closing
    def on_closing():
        if app.logger and hasattr(app.logger, 'stop_monitoring'):
            app.logger.stop_monitoring()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
