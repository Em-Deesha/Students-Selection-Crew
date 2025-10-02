#!/usr/bin/env python3
"""
Setup New Google Sheets Structure
This script sets up the proper structure in your new Google Sheets
"""

import os
import sys
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def setup_new_sheets_structure():
    """Set up the proper structure in the new Google Sheets"""
    
    # Set up credentials
    credentials_file = 'studentcrew-473406-c69f4c709523.json'
    if not os.path.exists(credentials_file):
        print(f"❌ Credentials file not found: {credentials_file}")
        return False
    
    try:
        # Authenticate
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        service = build('sheets', 'v4', credentials=creds)
        
        # Your new spreadsheet ID
        spreadsheet_id = '1JIh4vBLKoXoSKPFA4wHvC52HTlsqHQurvXqNCaiPsG4'
        
        print(f"🔧 Setting up structure in spreadsheet: {spreadsheet_id}")
        
        # Create new sheets
        create_sheets(service, spreadsheet_id)
        
        # Set up headers
        setup_headers(service, spreadsheet_id)
        
        print("✅ Successfully set up new Google Sheets structure!")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up structure: {e}")
        return False

def create_sheets(service, spreadsheet_id):
    """Create the required sheets"""
    try:
        # Get existing sheets
        spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        existing_sheets = [sheet['properties']['title'] for sheet in spreadsheet['sheets']]
        
        # Sheets to create
        required_sheets = ['Students', 'Quiz_Questions', 'Shortlisted_Students']
        
        for sheet_name in required_sheets:
            if sheet_name not in existing_sheets:
                # Create new sheet
                request_body = {
                    'requests': [{
                        'addSheet': {
                            'properties': {
                                'title': sheet_name,
                                'gridProperties': {
                                    'rowCount': 1000,
                                    'columnCount': 12
                                }
                            }
                        }
                    }]
                }
                
                service.spreadsheets().batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body=request_body
                ).execute()
                
                print(f"✅ Created sheet: {sheet_name}")
            else:
                print(f"ℹ️ Sheet already exists: {sheet_name}")
                
    except Exception as e:
        print(f"❌ Error creating sheets: {e}")

def setup_headers(service, spreadsheet_id):
    """Set up headers for all sheets"""
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
        
        print("✅ Set up headers for all sheets")
        
    except Exception as e:
        print(f"❌ Error setting up headers: {e}")

def main():
    """Main function"""
    print("🚀 Setting up new Google Sheets structure...")
    print("=" * 50)
    
    success = setup_new_sheets_structure()
    
    if success:
        print("\n" + "=" * 50)
        print("✅ SUCCESS! New Google Sheets structure is ready!")
        print("📊 Spreadsheet ID: 1JIh4vBLKoXoSKPFA4wHvC52HTlsqHQurvXqNCaiPsG4")
        print("🔗 URL: https://docs.google.com/spreadsheets/d/1JIh4vBLKoXoSKPFA4wHvC52HTlsqHQurvXqNCaiPsG4")
        print("\n📋 Structure Created:")
        print("   • Students - For student records and quiz answers")
        print("   • Quiz_Questions - For quiz questions and options")
        print("   • Shortlisted_Students - For shortlisted candidates")
        print("\n🔧 Next Steps:")
        print("   1. Restart your Streamlit application")
        print("   2. Test the new structure")
        print("   3. Create some quiz questions")
        print("   4. Add student data")
    else:
        print("\n❌ Failed to set up new Google Sheets structure")

if __name__ == "__main__":
    main()
