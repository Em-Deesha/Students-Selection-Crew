#!/usr/bin/env python3
"""
Setup New Google Sheets Structure for Student Selection System
This script creates a new Google Sheets with proper data organization
"""

import os
import sys
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def create_new_google_sheets_structure():
    """Create a new Google Sheets with proper structure"""
    
    # Set up credentials
    credentials_file = 'studentcrew-473406-c69f4c709523.json'
    if not os.path.exists(credentials_file):
        print(f"❌ Credentials file not found: {credentials_file}")
        return None, None
    
    try:
        # Authenticate
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        service = build('sheets', 'v4', credentials=creds)
        
        # Create new spreadsheet with proper structure
        spreadsheet_body = {
            'properties': {
                'title': 'Student Selection System - Clean Structure'
            },
            'sheets': [
                {
                    'properties': {
                        'title': 'Students',
                        'gridProperties': {
                            'rowCount': 1000,
                            'columnCount': 12
                        }
                    }
                },
                {
                    'properties': {
                        'title': 'Quiz_Questions',
                        'gridProperties': {
                            'rowCount': 100,
                            'columnCount': 10
                        }
                    }
                },
                {
                    'properties': {
                        'title': 'Shortlisted_Students',
                        'gridProperties': {
                            'rowCount': 100,
                            'columnCount': 12
                        }
                    }
                }
            ]
        }
        
        # Create the new spreadsheet
        spreadsheet = service.spreadsheets().create(body=spreadsheet_body).execute()
        spreadsheet_id = spreadsheet['spreadsheetId']
        spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
        
        print(f"✅ Created new Google Sheets with proper structure!")
        print(f"📊 Spreadsheet ID: {spreadsheet_id}")
        print(f"🔗 URL: {spreadsheet_url}")
        
        # Set up headers for each sheet
        setup_sheets_headers(service, spreadsheet_id)
        
        return spreadsheet_id, spreadsheet_url
        
    except Exception as e:
        print(f"❌ Error creating new Google Sheets: {e}")
        return None, None

def setup_sheets_headers(service, spreadsheet_id):
    """Set up headers for the new spreadsheet structure"""
    try:
        # Students sheet headers
        students_headers = [
            'Student_ID', 'Student_Name', 'Email', 'Quiz_Score', 'Status',
            'Student_Answers', 'Video_Link', 'Transcript', 'Confidence', 'AI_Experience', 'Final_Result'
        ]
        
        # Quiz Questions sheet headers
        quiz_headers = [
            'Question_ID', 'Question', 'Option_A', 'Option_B', 'Option_C', 'Option_D',
            'Correct_Answer', 'Points', 'Category', 'Difficulty'
        ]
        
        # Shortlisted Students sheet headers
        shortlisted_headers = [
            'Student_ID', 'Student_Name', 'Email', 'Quiz_Score', 'Status',
            'Student_Answers', 'Video_Link', 'Transcript', 'Confidence', 'AI_Experience', 'Final_Result'
        ]
        
        # Write headers to each sheet
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range='Students!A1:K1',
            valueInputOption='RAW',
            body={'values': [students_headers]}
        ).execute()
        
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range='Quiz_Questions!A1:J1',
            valueInputOption='RAW',
            body={'values': [quiz_headers]}
        ).execute()
        
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range='Shortlisted_Students!A1:K1',
            valueInputOption='RAW',
            body={'values': [shortlisted_headers]}
        ).execute()
        
        print("✅ Set up headers for all sheets in new structure")
        
    except Exception as e:
        print(f"❌ Error setting up new sheets headers: {e}")

def main():
    """Main function to create new Google Sheets structure"""
    print("🚀 Setting up new Google Sheets structure...")
    print("=" * 50)
    
    spreadsheet_id, spreadsheet_url = create_new_google_sheets_structure()
    
    if spreadsheet_id:
        print("\n" + "=" * 50)
        print("✅ SUCCESS! New Google Sheets created with proper structure")
        print(f"📊 Spreadsheet ID: {spreadsheet_id}")
        print(f"🔗 URL: {spreadsheet_url}")
        print("\n📋 Structure:")
        print("   • Students - For student records and quiz answers")
        print("   • Quiz_Questions - For quiz questions and options")
        print("   • Shortlisted_Students - For shortlisted candidates")
        print("\n🔧 Next Steps:")
        print("   1. Update your .env file with the new spreadsheet ID")
        print("   2. Update the frontend to use the new structure")
        print("   3. Test the new system")
    else:
        print("\n❌ Failed to create new Google Sheets structure")

if __name__ == "__main__":
    main()
