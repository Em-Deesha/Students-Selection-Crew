# 🔑 Google Cloud API Permissions Setup Guide

## Current Issue
Your service account doesn't have permission to create new Google Sheets because it only has access to the existing spreadsheet.

## Solution: Update Service Account Permissions

### Step 1: Go to Google Cloud Console
1. Visit: https://console.cloud.google.com/
2. Select your project: `studentcrew-473406`

### Step 2: Enable Required APIs
1. Go to **APIs & Services > Library**
2. Search and enable these APIs:
   - ✅ Google Sheets API (already enabled)
   - 🔄 Google Drive API (needed for creating files)
   - 🔄 Google Docs API (optional)

### Step 3: Update Service Account Permissions
1. Go to **IAM & Admin > Service Accounts**
2. Find your service account: `studentcrew-473406@studentcrew-473406.iam.gserviceaccount.com`
3. Click on it and go to **"Permissions"** tab
4. Click **"Add Role"** and add:
   - `Editor` (for full access)
   - `Google Sheets API` (if not already there)
   - `Google Drive API` (for creating files)

### Step 4: Download New Credentials (Optional)
If you want a fresh service account:
1. Go to **IAM & Admin > Service Accounts**
2. Click **"Create Service Account"**
3. Name: `student-selection-full-access`
4. Grant these roles:
   - `Editor`
   - `Google Sheets API`
   - `Google Drive API`
5. Create and download the JSON key
6. Replace your current `studentcrew-473406-c69f4c709523.json` file

## Alternative: Manual Google Sheets Creation

Since getting API permissions might take time, here's the manual approach:

### Step 1: Create New Google Sheets
1. Go to: https://sheets.google.com
2. Click **"Blank"** to create a new spreadsheet
3. Name it: `Student Selection System - Clean Structure`

### Step 2: Create Multiple Sheets
1. Click the **"+"** button at the bottom to add new sheets
2. Create these 3 sheets:
   - `Students`
   - `Quiz_Questions`
   - `Shortlisted_Students`

### Step 3: Set Up Headers

**Students Sheet Headers (Row 1):**
```
Student_ID | Student_Name | Email | Quiz_Score | Status | Student_Answers | Video_Link | Transcript | Confidence | AI_Experience | Final_Result
```

**Quiz_Questions Sheet Headers (Row 1):**
```
Question_ID | Question | Option_A | Option_B | Option_C | Option_D | Correct_Answer | Points | Category | Difficulty
```

**Shortlisted_Students Sheet Headers (Row 1):**
```
Student_ID | Student_Name | Email | Quiz_Score | Status | Student_Answers | Video_Link | Transcript | Confidence | AI_Experience | Final_Result
```

### Step 4: Get the New Spreadsheet ID
1. Copy the URL of your new spreadsheet
2. Extract the ID from the URL: `https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit`
3. Update your `.env` file with the new ID

### Step 5: Update Configuration
1. Open your `.env` file
2. Update the `GOOGLE_SHEETS_ID` with the new spreadsheet ID
3. Restart your application

## Quick Test
After setting up permissions or creating the new spreadsheet:
1. Run: `python setup_new_sheets.py` (if permissions are fixed)
2. Or manually create the structure and update your `.env` file
3. Test the application with the new structure

## Benefits of New Structure
- ✅ Clean separation of data
- ✅ Proper student answer storage
- ✅ No more mixed data issues
- ✅ Better organization and maintenance
- ✅ Easier to manage and debug
