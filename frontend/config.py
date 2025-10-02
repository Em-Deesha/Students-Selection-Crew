"""
Configuration settings for the Student Selection Crew
Supports both local .env files and Streamlit Cloud secrets
"""
import os
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

# Try to import streamlit for cloud deployment
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

def get_config_value(key, default=None):
    """Get configuration value from environment or Streamlit secrets"""
    # First try environment variables (local development)
    value = os.getenv(key, default)
    
    # If running on Streamlit Cloud, try secrets
    if STREAMLIT_AVAILABLE and hasattr(st, 'secrets') and value == default:
        try:
            value = st.secrets.get(key, default)
        except:
            pass
    
    return value

def get_google_credentials():
    """Get Google Service Account credentials from Streamlit secrets or file"""
    if STREAMLIT_AVAILABLE and hasattr(st, 'secrets'):
        try:
            # Try to get credentials from Streamlit secrets
            if 'google_service_account' in st.secrets:
                import json
                import tempfile
                
                # Create credentials dict from secrets
                creds_dict = dict(st.secrets['google_service_account'])
                
                # Write to temporary file for compatibility
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                    json.dump(creds_dict, f)
                    temp_file_path = f.name
                
                print(f"✅ Using Google Service Account from Streamlit secrets")
                return temp_file_path
        except Exception as e:
            print(f"⚠️ Error loading credentials from secrets: {e}")
    
    # Fallback to local file
    local_file = get_config_value('GOOGLE_CREDENTIALS_FILE', 'studentcrew-473406-c69f4c709523.json')
    if os.path.exists(local_file):
        print(f"✅ Using local credentials file: {local_file}")
        return local_file
    
    print(f"❌ No Google credentials found")
    return None

class Config:
    # API Keys
    OPENAI_API_KEY = get_config_value('OPENAI_API_KEY')
    GOOGLE_API_KEY = get_config_value('GOOGLE_API_KEY')
    GEMINI_API_KEY = get_config_value('GEMINI_API_KEY')
    ASSEMBLYAI_API_KEY = get_config_value('ASSEMBLYAI_API_KEY')
    
    # Google Services
    GOOGLE_CREDENTIALS_FILE = get_google_credentials()
    GOOGLE_SHEET_ID = get_config_value('GOOGLE_SHEET_ID', '1JIh4vBLKoXoSKPFA4wHvC52HTlsqHQurvXqNCaiPsG4')
    GOOGLE_DRIVE_FOLDER_ID = get_config_value('GOOGLE_DRIVE_FOLDER_ID')
    
    # Email Configuration
    GMAIL_USERNAME = get_config_value('GMAIL_USERNAME')
    GMAIL_APP_PASSWORD = get_config_value('GMAIL_APP_PASSWORD')
    
    # Project Settings
    PROJECT_NAME = get_config_value('PROJECT_NAME', 'Student Selection Crew')
    MAX_SHORTLIST = int(get_config_value('MAX_SHORTLIST', '10'))
    MAX_FINAL_SELECTION = int(get_config_value('MAX_FINAL_SELECTION', '5'))
    
    # File Paths
    DATA_DIR = 'data'
    OUTPUTS_DIR = 'outputs'
    TEMP_DIR = 'temp'
    
    # Email Templates
    SHORTLIST_EMAIL_TEMPLATE = """
    Congratulations! You have been shortlisted for the next round.
    
    Please upload a 1-minute video interview at the following link:
    {drive_link}
    
    The video should cover:
    - Your background and experience
    - Why you're interested in AI/ML
    - Your current education status
    
    Deadline: {deadline}
    """
    
    FINAL_SELECTION_EMAIL_TEMPLATE = """
    🎉 Congratulations! 
    
    You have been selected for the AgenticAI course! 
    
    We were impressed by your quiz performance and video interview. Your dedication and skills have earned you a spot in our program.
    
    📚 Course details will be shared with you shortly via email.
    
    We're excited to have you join our AgenticAI learning community!
    """
