"""
Fix the Google Sheets structure to work with your existing sheet
"""
from tools.sheets_manager import SheetsManager
from config import Config

def fix_sheet_structure():
    """Fix the sheet structure to work with your existing sheet"""
    print("🔧 FIXING GOOGLE SHEETS STRUCTURE")
    print("=" * 40)
    
    try:
        # Initialize sheets manager
        sheets_manager = SheetsManager(
            Config.GOOGLE_CREDENTIALS_FILE,
            Config.GOOGLE_SHEET_ID
        )
        
        # Your existing sheet structure
        print("📊 Your existing sheet structure:")
        print("Student Name | Email | Quiz Marks | Status | Video Link | Transcript | Confidence | AI Experience | Final Result")
        
        # Create headers for your existing sheet
        headers = [
            'Student Name', 'Email', 'Quiz Marks', 'Status', 
            'Video Link', 'Transcript', 'Confidence', 'AI Experience', 'Final Result'
        ]
        
        # Check if headers already exist
        try:
            existing_data = sheets_manager.read_sheet('Sheet1', 'A1:I1')
            if existing_data and existing_data[0] == headers:
                print("✅ Headers already exist and match!")
                return True
        except:
            pass
        
        # Add headers to your sheet
        print("📝 Adding headers to your sheet...")
        sheets_manager.write_sheet('Sheet1', [headers], 'A1')
        print("✅ Headers added successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing sheet structure: {e}")
        return False

def test_sheet_connection():
    """Test the sheet connection"""
    print("\n🧪 TESTING SHEET CONNECTION")
    print("=" * 40)
    
    try:
        from tools.sheets_manager import SheetsManager
        
        sheets_manager = SheetsManager(
            Config.GOOGLE_CREDENTIALS_FILE,
            Config.GOOGLE_SHEET_ID
        )
        
        # Test reading from your sheet
        data = sheets_manager.read_sheet('Sheet1', 'A1:I1')
        print("✅ Successfully connected to your Google Sheet!")
        print(f"📊 Found {len(data)} rows")
        
        if data:
            print("📋 Current data:")
            for i, row in enumerate(data[:3]):  # Show first 3 rows
                print(f"  Row {i+1}: {row}")
        
        return True
        
    except Exception as e:
        print(f"❌ Sheet connection failed: {e}")
        return False

def main():
    """Fix the sheet structure"""
    print("🚀 FIXING YOUR GOOGLE SHEETS INTEGRATION")
    print("=" * 50)
    
    # Test connection first
    if test_sheet_connection():
        # Fix the structure
        if fix_sheet_structure():
            print("\n🎉 SUCCESS!")
            print("Your Google Sheets integration is now working!")
            print("\nYour sheet is ready for the Student Selection Crew!")
        else:
            print("\n❌ Failed to fix sheet structure")
    else:
        print("\n❌ Cannot connect to Google Sheets")
        print("Please check:")
        print("1. Your credentials file is correct")
        print("2. Your Google Sheet is shared with the service account")
        print("3. Your Google API key is valid")

if __name__ == "__main__":
    main()
