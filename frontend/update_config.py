#!/usr/bin/env python3
"""
Update Configuration for New Google Sheets Structure
This script helps you update your configuration with the new spreadsheet ID
"""

import os

def update_config_with_new_sheets():
    """Update configuration with new Google Sheets ID"""
    
    print("🔧 Configuration Update Helper")
    print("=" * 50)
    
    # Get new spreadsheet ID from user
    new_sheet_id = input("Enter your new Google Sheets ID (from the URL): ").strip()
    
    if not new_sheet_id:
        print("❌ No spreadsheet ID provided!")
        return
    
    # Create .env file with new configuration
    env_content = f"""# Student Selection Crew Configuration
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here

# Google Services
GOOGLE_CREDENTIALS_FILE=studentcrew-473406-c69f4c709523.json
GOOGLE_SHEET_ID={new_sheet_id}
GOOGLE_DRIVE_FOLDER_ID=your_drive_folder_id_here

# Email Configuration
GMAIL_USERNAME=your_email@gmail.com
GMAIL_APP_PASSWORD=your_app_password_here

# Project Settings
PROJECT_NAME=Student Selection Crew
MAX_SHORTLIST=10
MAX_FINAL_SELECTION=5
"""
    
    # Write to .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print(f"✅ Updated .env file with new spreadsheet ID: {new_sheet_id}")
    print("\n📋 Next Steps:")
    print("1. Update your API keys in the .env file")
    print("2. Set up your Google Drive folder ID")
    print("3. Configure your email settings")
    print("4. Restart your application")
    
    # Also update the config.py file to use the new ID
    config_content = f'''"""
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
    GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID', '{new_sheet_id}')
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
    {{drive_link}}
    
    The video should cover:
    - Your background and experience
    - Why you're interested in AI/ML
    - Your current education status
    
    Deadline: {{deadline}}
    """
    
    FINAL_SELECTION_EMAIL_TEMPLATE = """
    Congratulations! You have been selected for the final round.
    
    We were impressed by your video interview and would like to proceed with the next steps.
    
    Please check your email for further instructions.
    """
'''
    
    with open('config.py', 'w') as f:
        f.write(config_content)
    
    print("✅ Updated config.py file")
    print("\n🎯 Your new Google Sheets structure is ready!")
    print("📊 Spreadsheet ID:", new_sheet_id)
    print("🔗 URL: https://docs.google.com/spreadsheets/d/" + new_sheet_id)

if __name__ == "__main__":
    update_config_with_new_sheets()
