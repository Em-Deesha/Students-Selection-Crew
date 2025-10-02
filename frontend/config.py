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

class Config:
    # API Keys
    OPENAI_API_KEY = get_config_value('OPENAI_API_KEY')
    GOOGLE_API_KEY = get_config_value('GOOGLE_API_KEY')
    GEMINI_API_KEY = get_config_value('GEMINI_API_KEY')
    ASSEMBLYAI_API_KEY = get_config_value('ASSEMBLYAI_API_KEY')
    
    # Google Services
    GOOGLE_CREDENTIALS_FILE = get_config_value('GOOGLE_CREDENTIALS_FILE', 'studentcrew-473406-c69f4c709523.json')
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
