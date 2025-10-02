#!/usr/bin/env python3
"""
Script to clear corrupted data from Google Sheets and start fresh
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.sheets_manager import SheetsManager
from config import Config

def clear_students_sheet():
    """Clear all data from Students sheet except headers"""
    try:
        # Initialize sheets manager
        sheets_manager = SheetsManager(Config.GOOGLE_SHEET_ID, Config.GOOGLE_CREDENTIALS_FILE)
        
        print("🧹 Clearing corrupted data from Students sheet...")
        
        # Clear all data except header row
        sheets_manager.clear_sheet('Students', 'A2:K1000')  # Clear data rows, keep header
        
        print("✅ Students sheet cleared successfully!")
        print("📋 The sheet now has only the header row with proper column structure:")
        print("   A: Student_ID")
        print("   B: Student_Name") 
        print("   C: Email")
        print("   D: Quiz_Score")
        print("   E: Status")
        print("   F: Student_Answers")
        print("   G: Video_Link")
        print("   H: Transcript")
        print("   I: Confidence")
        print("   J: AI_Experience")
        print("   K: Final_Result")
        
        return True
        
    except Exception as e:
        print(f"❌ Error clearing Students sheet: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Google Sheets Data Cleanup Tool")
    print("=" * 50)
    
    # Clear Students sheet
    if clear_students_sheet():
        print("\n✅ Data cleanup completed successfully!")
        print("\n📝 Next steps:")
        print("1. Go to your Google Sheets and verify the data is cleared")
        print("2. Restart the Streamlit application")
        print("3. Add new students and test the quiz functionality")
        print("4. Check that quiz scores are properly saved")
    else:
        print("\n❌ Data cleanup failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
