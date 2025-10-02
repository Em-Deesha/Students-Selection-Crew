#!/usr/bin/env python3
"""
Quick launcher for the Student Selection Crew Demo
"""
import subprocess
import sys
import os

def main():
    print("🎓 Student Selection Crew - Demo Launcher")
    print("=" * 50)
    print("Starting the interactive web interface...")
    print("The demo will open in your browser at: http://localhost:8501")
    print("Press Ctrl+C to stop the demo")
    print("=" * 50)
    
    try:
        # Run the demo app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "demo_app.py",
            "--server.port", "8501",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Demo stopped. Thank you for trying Student Selection Crew!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure you have streamlit installed: pip install streamlit")

if __name__ == "__main__":
    main()
