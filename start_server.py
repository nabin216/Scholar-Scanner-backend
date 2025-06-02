#!/usr/bin/env python
"""
Start Django server and create a simple test endpoint
"""

import subprocess
import time
import webbrowser
import sys

def start_server():
    """Start Django development server"""
    print("Starting Django development server...")
    
    # Start the server
    try:
        process = subprocess.Popen([
            sys.executable, 'manage.py', 'runserver', '8000'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("Server starting... waiting 3 seconds")
        time.sleep(3)
        
        print("Server should be running at http://localhost:8000")
        print("You can test the email verification at:")
        print("http://localhost:8000/api/auth/send-verification-email/")
        
        return process
        
    except Exception as e:
        print(f"Error starting server: {e}")
        return None

if __name__ == "__main__":
    server_process = start_server()
    
    if server_process:
        try:
            print("\nPress Ctrl+C to stop the server")
            server_process.wait()
        except KeyboardInterrupt:
            print("\nStopping server...")
            server_process.terminate()
            server_process.wait()
            print("Server stopped.")
