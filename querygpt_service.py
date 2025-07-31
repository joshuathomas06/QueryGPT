#!/usr/bin/env python3
"""
QueryGPT Service Manager - Keeps both API and Frontend running
"""

import subprocess
import time
import signal
import sys
import os
from datetime import datetime

class QueryGPTService:
    def __init__(self):
        self.api_process = None
        self.frontend_process = None
        self.running = True
        
    def log(self, message):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def start_api(self):
        """Start API server"""
        self.log("🚀 Starting API server...")
        try:
            self.api_process = subprocess.Popen(
                ["python", "api.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            self.log(f"✅ API started (PID: {self.api_process.pid})")
        except Exception as e:
            self.log(f"❌ Failed to start API: {e}")
            
    def start_frontend(self):
        """Start frontend server"""
        self.log("🎨 Starting frontend...")
        try:
            os.chdir("frontend")
            self.frontend_process = subprocess.Popen(
                ["npm", "start"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env={**os.environ, "BROWSER": "none"}  # Don't auto-open browser
            )
            os.chdir("..")
            self.log(f"✅ Frontend started (PID: {self.frontend_process.pid})")
        except Exception as e:
            self.log(f"❌ Failed to start frontend: {e}")
            
    def check_api_health(self):
        """Check if API is responding"""
        try:
            result = subprocess.run(
                ["curl", "-s", "http://localhost:8000/health"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
            
    def monitor_services(self):
        """Monitor and restart services if needed"""
        while self.running:
            # Check API
            if self.api_process and self.api_process.poll() is not None:
                self.log("⚠️  API crashed, restarting...")
                time.sleep(5)
                self.start_api()
            elif not self.api_process:
                self.start_api()
                
            # Check Frontend
            if self.frontend_process and self.frontend_process.poll() is not None:
                self.log("⚠️  Frontend crashed, restarting...")
                time.sleep(5)
                self.start_frontend()
            elif not self.frontend_process:
                self.start_frontend()
                
            # Wait before next check
            time.sleep(10)
            
    def stop(self):
        """Stop all services"""
        self.log("🛑 Stopping services...")
        self.running = False
        
        if self.api_process:
            self.api_process.terminate()
            self.api_process.wait()
            
        if self.frontend_process:
            self.frontend_process.terminate()
            self.frontend_process.wait()
            
        # Clean up any remaining processes
        subprocess.run(["pkill", "-f", "python api.py"], capture_output=True)
        subprocess.run(["pkill", "-f", "npm start"], capture_output=True)
        
        self.log("✅ All services stopped")
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.stop()
        sys.exit(0)
        
    def run(self):
        """Main service loop"""
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        self.log("🚀 QueryGPT Service Manager starting...")
        self.log("Press Ctrl+C to stop")
        
        # Wait for API to be ready
        self.start_api()
        self.log("⏳ Waiting for API to initialize...")
        
        for _ in range(60):
            if self.check_api_health():
                self.log("✅ API is ready!")
                break
            time.sleep(2)
        
        # Start frontend
        self.start_frontend()
        
        self.log("✅ All services started!")
        self.log("📊 API: http://localhost:8000")
        self.log("🌐 Frontend: http://localhost:3000")
        
        # Monitor services
        self.monitor_services()

if __name__ == "__main__":
    service = QueryGPTService()
    service.run()