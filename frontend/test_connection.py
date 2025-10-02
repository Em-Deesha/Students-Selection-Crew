"""
Test script to verify the frontend can connect to the backend
"""
import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from config import Config
        print("✅ Config imported successfully")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from fixed_student_selection_crew import FixedStudentSelectionCrew
        print("✅ FixedStudentSelectionCrew imported successfully")
    except ImportError as e:
        print(f"❌ FixedStudentSelectionCrew import failed: {e}")
        return False
    
    return True

def test_credentials():
    """Test if credentials file exists"""
    print("\n🔑 Testing credentials...")
    
    creds_file = "studentcrew-473406-c69f4c709523.json"
    
    if os.path.exists(creds_file):
        print(f"✅ Credentials file found: {creds_file}")
        return True
    else:
        print(f"❌ Credentials file not found: {creds_file}")
        return False

def test_config():
    """Test configuration values"""
    print("\n⚙️ Testing configuration...")
    
    try:
        from config import Config
        
        print(f"✅ Google Sheet ID: {Config.GOOGLE_SHEET_ID}")
        print(f"✅ Gmail Username: {Config.GMAIL_USERNAME}")
        print(f"✅ Max Shortlist: {Config.MAX_SHORTLIST}")
        print(f"✅ Max Final Selection: {Config.MAX_FINAL_SELECTION}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_crew_initialization():
    """Test crew initialization"""
    print("\n🚀 Testing crew initialization...")
    
    try:
        from fixed_student_selection_crew import FixedStudentSelectionCrew
        from config import Config
        
        crew = FixedStudentSelectionCrew(
            credentials_file="studentcrew-473406-c69f4c709523.json",
            sheet_id=Config.GOOGLE_SHEET_ID,
            gmail_username=Config.GMAIL_USERNAME,
            gmail_password=Config.GMAIL_APP_PASSWORD
        )
        
        print("✅ Crew initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Crew initialization failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🎓 Student Selection Crew - Frontend Connection Test")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Credentials Test", test_credentials),
        ("Configuration Test", test_config),
        ("Crew Initialization Test", test_crew_initialization)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 60)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your frontend is ready to use!")
        print("\n🚀 To start the frontend:")
        print("   streamlit run app.py")
        print("\n🌐 Then open: http://localhost:8501")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure all files are in the frontend directory")
        print("2. Check that credentials file exists")
        print("3. Verify configuration values")
        print("4. Install required dependencies: pip install -r requirements.txt")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
