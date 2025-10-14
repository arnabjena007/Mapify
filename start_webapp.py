#!/usr/bin/env python3
"""
Startup script for Kolkata City Pathfinder Web Application
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import flask
        import flask_cors
        from kolkata_pathfinder import KolkataPathfinder
        print("✅ All dependencies are available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def start_web_app():
    """Start the Flask web application"""
    print("🚀 Starting Kolkata City Pathfinder Web Application...")
    print("=" * 60)
    
    if not check_dependencies():
        return False
    
    # Check if templates and static directories exist
    templates_dir = Path("templates")
    static_dir = Path("static")
    
    if not templates_dir.exists():
        print("❌ Templates directory not found")
        return False
    
    if not static_dir.exists():
        print("❌ Static directory not found")
        return False
    
    print("📁 Directory structure verified")
    print("🏙️  Initializing Kolkata pathfinder (this may take a few minutes)...")
    
    try:
        # Start the Flask app
        from web_app import app, initialize_pathfinder
        
        # Initialize pathfinder
        if not initialize_pathfinder():
            print("❌ Failed to initialize pathfinder")
            return False
        
        print("✅ Pathfinder initialized successfully!")
        print("🌐 Starting web server...")
        print()
        print("🎉 Web application is ready!")
        print("📱 Open your browser and go to: http://localhost:8080")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Try to open browser automatically
        try:
            webbrowser.open('http://localhost:8080')
            print("🌐 Browser opened automatically")
        except:
            print("💡 Please manually open http://localhost:8080 in your browser")
        
        # Start Flask app
        app.run(debug=False, host='0.0.0.0', port=8080)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error starting web app: {e}")
        return False

if __name__ == "__main__":
    success = start_web_app()
    sys.exit(0 if success else 1)
