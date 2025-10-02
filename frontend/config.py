"""
Configuration settings for the Student Selection Crew
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')
    
    # Google Services
    GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'studentcrew-473406-c69f4c709523.json')
    GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID', '1JIh4vBLKoXoSKPFA4wHvC52HTlsqHQurvXqNCaiPsG4')
    GOOGLE_DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    
    # Email Configuration
    GMAIL_USERNAME = os.getenv('GMAIL_USERNAME')
    GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
    
    # Project Settings
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'Student Selection Crew')
    MAX_SHORTLIST = int(os.getenv('MAX_SHORTLIST', 10))
    MAX_FINAL_SELECTION = int(os.getenv('MAX_FINAL_SELECTION', 5))
    
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
