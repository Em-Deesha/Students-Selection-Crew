"""
Google Sheets management tool for storing and retrieving data
"""
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from typing import List, Dict, Any
import os

class SheetsManager:
    def __init__(self, credentials_file: str, sheet_id: str):
        """
        Initialize Google Sheets manager
        
        Args:
            credentials_file: Path to Google service account credentials
            sheet_id: Google Sheets document ID
        """
        self.credentials_file = credentials_file
        self.sheet_id = sheet_id
        self.service = self._build_service()
    
    def _build_service(self):
        """Build Google Sheets service"""
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(
            self.credentials_file, scopes=scopes
        )
        return build('sheets', 'v4', credentials=creds)
    
    def read_sheet(self, sheet_name: str, range_name: str = None) -> List[List[str]]:
        """
        Read data from Google Sheets
        
        Args:
            sheet_name: Name of the sheet
            range_name: Range to read (e.g., 'A1:Z100')
        
        Returns:
            List of rows from the sheet
        """
        if range_name:
            range_to_read = f"{sheet_name}!{range_name}"
        else:
            range_to_read = sheet_name
        
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id,
            range=range_to_read
        ).execute()
        
        return result.get('values', [])
    
    def write_sheet(self, sheet_name: str, data: List[List[str]], 
                   start_cell: str = 'A1') -> None:
        """
        Write data to Google Sheets
        
        Args:
            sheet_name: Name of the sheet
            data: List of rows to write
            start_cell: Starting cell (e.g., 'A1')
        """
        range_to_write = f"{sheet_name}!{start_cell}"
        
        body = {'values': data}
        self.service.spreadsheets().values().update(
            spreadsheetId=self.sheet_id,
            range=range_to_write,
            valueInputOption='RAW',
            body=body
        ).execute()
    
    def append_to_sheet(self, sheet_name: str, data: List[List[str]]) -> None:
        """
        Append data to the end of a sheet
        
        Args:
            sheet_name: Name of the sheet
            data: List of rows to append
        """
        range_to_append = f"{sheet_name}!A:Z"
        
        body = {'values': data}
        self.service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id,
            range=range_to_append,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
    
    def update_cell(self, sheet_name: str, cell: str, value: str) -> None:
        """
        Update a specific cell
        
        Args:
            sheet_name: Name of the sheet
            cell: Cell reference (e.g., 'A1')
            value: Value to write
        """
        range_to_update = f"{sheet_name}!{cell}"
        
        body = {'values': [[value]]}
        self.service.spreadsheets().values().update(
            spreadsheetId=self.sheet_id,
            range=range_to_update,
            valueInputOption='RAW',
            body=body
        ).execute()
