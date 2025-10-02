"""
Simple launcher for the Student Selection Crew Frontend
"""
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def run_streamlit():
    """Run the Streamlit app"""
    print("🚀 Starting Student Selection Crew Frontend...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ Error running app: {e}")

def main():
    """Main launcher function"""
    print("🎓 Student Selection Crew - Frontend Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ app.py not found. Please run this from the frontend directory.")
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Run the app
    run_streamlit()

if __name__ == "__main__":
    main()
