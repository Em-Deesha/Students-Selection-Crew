"""
Test script to verify API configuration
"""
import os
from dotenv import load_dotenv

def test_api_configuration():
    """Test if all required APIs are configured"""
    print("=== API CONFIGURATION TEST ===")
    print("Testing your API setup...")
    
    # Load environment variables
    load_dotenv()
    
    # Test each API key
    apis = {
        "OpenAI API": os.getenv('OPENAI_API_KEY'),
        "Google API": os.getenv('GOOGLE_API_KEY'),
        "Gemini API": os.getenv('GEMINI_API_KEY'),
        "AssemblyAI API": os.getenv('ASSEMBLYAI_API_KEY'),
        "Gmail Username": os.getenv('GMAIL_USERNAME'),
        "Gmail App Password": os.getenv('GMAIL_APP_PASSWORD'),
        "Google Sheet ID": os.getenv('GOOGLE_SHEET_ID'),
        "Google Credentials File": os.getenv('GOOGLE_CREDENTIALS_FILE')
    }
    
    print("\n--- API Status ---")
    all_configured = True
    
    for api_name, api_value in apis.items():
        if api_value and api_value != f"your_{api_name.lower().replace(' ', '_')}_here":
            print(f"✓ {api_name}: Configured")
        else:
            print(f"✗ {api_name}: Not configured")
            all_configured = False
    
    print("\n--- Configuration Summary ---")
    if all_configured:
        print("🎉 All APIs are configured! Your system is ready to use.")
        return True
    else:
        print("❌ Some APIs are missing. Please check your .env file.")
        print("\nRequired APIs:")
        print("1. OpenAI API Key (for AI analysis)")
        print("2. Google API Key (for Google Sheets)")
        print("3. Gmail credentials (for sending emails)")
        print("4. Google Sheet ID (your specific sheet)")
        return False

def test_google_sheet_connection():
    """Test Google Sheets connection"""
    print("\n=== GOOGLE SHEETS CONNECTION TEST ===")
    
    try:
        from tools.sheets_manager import SheetsManager
        
        # Check if credentials file exists
        credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
        sheet_id = os.getenv('GOOGLE_SHEET_ID')
        
        if not os.path.exists(credentials_file):
            print(f"✗ Credentials file not found: {credentials_file}")
            print("Please download your Google service account credentials and save as 'credentials.json'")
            return False
        
        if not sheet_id:
            print("✗ Google Sheet ID not configured")
            return False
        
        print(f"✓ Credentials file found: {credentials_file}")
        print(f"✓ Sheet ID configured: {sheet_id}")
        
        # Try to initialize the sheets manager
        try:
            sheets_manager = SheetsManager(credentials_file, sheet_id)
            print("✓ Google Sheets connection successful!")
            return True
        except Exception as e:
            print(f"✗ Google Sheets connection failed: {e}")
            print("Please check:")
            print("1. Your credentials.json file is correct")
            print("2. Your Google Sheet is shared with the service account")
            print("3. Your Google API key is valid")
            return False
            
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_email_configuration():
    """Test email configuration"""
    print("\n=== EMAIL CONFIGURATION TEST ===")
    
    try:
        from tools.email_manager import EmailManager
        
        gmail_username = os.getenv('GMAIL_USERNAME')
        gmail_password = os.getenv('GMAIL_APP_PASSWORD')
        
        if not gmail_username or not gmail_password:
            print("✗ Gmail credentials not configured")
            return False
        
        print(f"✓ Gmail username: {gmail_username}")
        print(f"✓ Gmail app password: {'*' * len(gmail_password)}")
        
        # Try to initialize email manager
        try:
            email_manager = EmailManager(gmail_username, gmail_password)
            print("✓ Email manager initialized successfully!")
            return True
        except Exception as e:
            print(f"✗ Email manager initialization failed: {e}")
            return False
            
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def main():
    """Run all API tests"""
    print("🔍 TESTING YOUR API CONFIGURATION")
    print("=" * 50)
    
    # Test API configuration
    api_configured = test_api_configuration()
    
    if api_configured:
        # Test Google Sheets connection
        sheets_ok = test_google_sheet_connection()
        
        # Test email configuration
        email_ok = test_email_configuration()
        
        print("\n" + "=" * 50)
        print("📊 FINAL RESULTS")
        print("=" * 50)
        
        if sheets_ok and email_ok:
            print("🎉 ALL SYSTEMS READY!")
            print("Your Student Selection Crew is fully configured and ready to use!")
            print("\nNext steps:")
            print("1. Run: python example_usage.py")
            print("2. Start creating quiz questions")
            print("3. Begin the selection process")
        else:
            print("⚠️  PARTIAL CONFIGURATION")
            print("Some components need attention:")
            if not sheets_ok:
                print("- Google Sheets connection needs fixing")
            if not email_ok:
                print("- Email configuration needs fixing")
    else:
        print("\n❌ API CONFIGURATION INCOMPLETE")
        print("Please configure your APIs in the .env file first.")

if __name__ == "__main__":
    main()
