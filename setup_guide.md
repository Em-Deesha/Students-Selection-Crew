# Setup Guide for Student Selection Crew

This guide will walk you through setting up the Student Selection Crew system step by step.

## Prerequisites

Before starting, ensure you have:
- Python 3.8 or higher
- A Google account
- A Gmail account
- Access to OpenAI API
- Basic understanding of APIs and credentials

## Step 1: Environment Setup

### 1.1 Create Virtual Environment
```bash
# Navigate to your project directory
cd /path/to/Crewai

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 1.2 Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 2: Google Cloud Setup

### 2.1 Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name: "Student Selection Crew"
4. Click "Create"

### 2.2 Enable Required APIs
1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search and enable:
   - Google Sheets API
   - Google Drive API
   - Gmail API

### 2.3 Create Service Account
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Enter name: "student-selection-service"
4. Click "Create and Continue"
5. Skip role assignment for now
6. Click "Done"

### 2.4 Generate Service Account Key
1. Click on your service account
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose "JSON" format
5. Download the key file
6. Rename it to `credentials.json`
7. Place it in your project root directory

## Step 3: Google Sheets Setup

### 3.1 Create Google Sheet
1. Go to [Google Sheets](https://sheets.google.com/)
2. Create a new spreadsheet
3. Name it "Student Selection Data"
4. Copy the Sheet ID from the URL (the long string between `/d/` and `/edit`)

### 3.2 Share Sheet with Service Account
1. Click "Share" button in your Google Sheet
2. Add the service account email (from credentials.json)
3. Give "Editor" permissions
4. Click "Send"

## Step 4: Gmail Setup

### 4.1 Enable 2-Factor Authentication
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Click "Security"
3. Enable "2-Step Verification"

### 4.2 Generate App Password
1. In Google Account Settings, go to "Security"
2. Click "App passwords"
3. Select "Mail" and "Other (custom name)"
4. Enter "Student Selection Crew"
5. Click "Generate"
6. Copy the 16-character password

## Step 5: API Keys Setup

### 5.1 OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to "API Keys"
4. Click "Create new secret key"
5. Copy the key

### 5.2 Google Gemini API Key (Optional)
1. Go to [Google AI Studio](https://makersuite.google.com/)
2. Click "Get API key"
3. Create a new API key
4. Copy the key

### 5.3 AssemblyAI API Key (Optional)
1. Go to [AssemblyAI](https://www.assemblyai.com/)
2. Sign up for free account
3. Go to "API Keys"
4. Copy your API key

## Step 6: Environment Configuration

### 6.1 Create .env File
```bash
# Copy the example file
cp .env.example .env
```

### 6.2 Fill in .env File
Edit the `.env` file with your credentials:

```env
# API Keys
OPENAI_API_KEY=sk-your-openai-key-here
GOOGLE_API_KEY=your-google-api-key-here
GEMINI_API_KEY=your-gemini-key-here
ASSEMBLYAI_API_KEY=your-assemblyai-key-here

# Google Services
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_ID=your-google-sheet-id-here
GOOGLE_DRIVE_FOLDER_ID=your-drive-folder-id-here

# Email Configuration
GMAIL_USERNAME=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password

# Project Settings
PROJECT_NAME=Student Selection Crew
MAX_SHORTLIST=10
MAX_FINAL_SELECTION=5
```

## Step 7: Test the System

### 7.1 Run System Test
```bash
python test_system.py
```

### 7.2 Run Example Usage
```bash
python example_usage.py
```

## Step 8: Google Drive Setup (Optional)

### 8.1 Create Drive Folder
1. Go to [Google Drive](https://drive.google.com/)
2. Create a new folder: "Student Video Interviews"
3. Copy the folder ID from the URL

### 8.2 Share Folder
1. Right-click the folder
2. Click "Share"
3. Add the service account email
4. Give "Editor" permissions

## Troubleshooting

### Common Issues

1. **"Credentials not found" error**
   - Ensure `credentials.json` is in the project root
   - Check the file path in `.env`

2. **"Sheet not accessible" error**
   - Verify the service account email has access to the sheet
   - Check the sheet ID is correct

3. **"Email sending failed" error**
   - Verify Gmail app password is correct
   - Ensure 2-factor authentication is enabled

4. **"API key invalid" error**
   - Check API keys are correctly copied
   - Verify API keys are active and have sufficient quota

5. **"Video analysis failed" error**
   - Install FFmpeg: `sudo apt-get install ffmpeg`
   - Check video file format and path

### Verification Checklist

- [ ] Virtual environment activated
- [ ] All dependencies installed
- [ ] Google Cloud project created
- [ ] APIs enabled
- [ ] Service account created
- [ ] Credentials downloaded
- [ ] Google Sheet created and shared
- [ ] Gmail 2FA enabled
- [ ] App password generated
- [ ] API keys obtained
- [ ] .env file configured
- [ ] System test passed

## Next Steps

Once setup is complete:

1. **Test the system** with sample data
2. **Customize the selection criteria** if needed
3. **Set up monitoring** for the selection process
4. **Create backup procedures** for data
5. **Train your team** on using the system

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the error messages carefully
3. Verify all credentials and permissions
4. Test each component individually
5. Check the logs for detailed error information

For additional help, refer to the main README.md file or create an issue in the repository.
