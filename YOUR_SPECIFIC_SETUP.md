# 🎯 Your Specific Setup Instructions

## 📊 Your Google Sheet Analysis

**Your Sheet URL**: `https://docs.google.com/spreadsheets/d/1UoGodmpxsuAUB9BzL7ILYWWNRw5tOiqKnAkxdvl6Wm8/edit`

**Sheet ID**: `1UoGodmpxsuAUB9BzL7ILYWWNRw5tOiqKnAkxdvl6Wm8`

**Your Column Structure**:
```
Student Name | Email | Quiz Marks | Status | Video Link | Transcript | Confidence | AI Experience | Final Result
```

✅ **Perfect!** This matches exactly what our system needs!

## 🔑 **REQUIRED APIs for Your Setup**

### 1. **OpenAI API** (MUST HAVE)
- **Cost**: ~$5-20/month
- **Get from**: https://platform.openai.com/api-keys
- **Why needed**: AI analysis of video transcripts
- **Add to .env**: `OPENAI_API_KEY=sk-your-key-here`

### 2. **Google Cloud Setup** (MUST HAVE)
- **Cost**: FREE
- **Steps**:
  1. Go to https://console.cloud.google.com/
  2. Create project: "Student Selection Crew"
  3. Enable APIs: Google Sheets API, Gmail API
  4. Create Service Account → Download `credentials.json`
  5. **IMPORTANT**: Share your Google Sheet with the service account email
  6. Get API key from Credentials section
  7. Add to .env: `GOOGLE_API_KEY=your-google-key`

### 3. **Gmail App Password** (MUST HAVE)
- **Cost**: FREE
- **Steps**:
  1. Go to https://myaccount.google.com/security
  2. Enable 2-Step Verification
  3. Go to App passwords → Create new
  4. Select "Mail" → Name: "Student Selection Crew"
  5. Copy the 16-character password
  6. Add to .env: `GMAIL_APP_PASSWORD=your-16-char-password`

## 📝 **Your .env File Should Look Like This**

```env
# ===========================================
# YOUR SPECIFIC CONFIGURATION
# ===========================================

# API Keys (Replace with your actual keys)
OPENAI_API_KEY=sk-your-actual-openai-key-here
GOOGLE_API_KEY=your-actual-google-api-key-here
GEMINI_API_KEY=your-gemini-key-here
ASSEMBLYAI_API_KEY=your-assemblyai-key-here

# Google Services (Your specific sheet)
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_ID=1UoGodmpxsuAUB9BzL7ILYWWNRw5tOiqKnAkxdvl6Wm8
GOOGLE_DRIVE_FOLDER_ID=your-drive-folder-id-here

# Email Configuration (Your email)
GMAIL_USERNAME=your-actual-email@gmail.com
GMAIL_APP_PASSWORD=your-actual-16-character-password

# Project Settings
PROJECT_NAME=Student Selection Crew
MAX_SHORTLIST=10
MAX_FINAL_SELECTION=5
```

## 🚀 **Step-by-Step Setup for Your System**

### Step 1: Install Dependencies
```bash
cd /home/adeesha-waheed/Documents/Crewai
pip install -r requirements.txt
```

### Step 2: Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign up/Login
3. Create new secret key
4. Copy the key (starts with `sk-`)
5. Update `.env`: `OPENAI_API_KEY=sk-your-key-here`

### Step 3: Set Up Google Cloud
1. Go to https://console.cloud.google.com/
2. Create new project: "Student Selection Crew"
3. Enable APIs:
   - Google Sheets API
   - Gmail API
4. Create Service Account:
   - Go to "Credentials" → "Create Credentials" → "Service Account"
   - Name: "student-selection-service"
   - Download JSON → save as `credentials.json` in your project folder
5. **CRITICAL**: Share your Google Sheet with the service account email
6. Get API key from "Credentials" → "Create Credentials" → "API Key"
7. Update `.env`: `GOOGLE_API_KEY=your-google-key`

### Step 4: Set Up Gmail
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Go to "App passwords"
4. Create new app password for "Student Selection Crew"
5. Copy the 16-character password
6. Update `.env`: `GMAIL_APP_PASSWORD=your-16-char-password`

### Step 5: Test Your Setup
```bash
python test_system.py
```

## 🎯 **How Your Sheet Will Be Used**

Your Google Sheet columns will be populated as follows:

| Column | How It's Filled | When |
|--------|----------------|------|
| **Student Name** | Manual entry | When students register |
| **Email** | Manual entry | When students register |
| **Quiz Marks** | Auto-filled by Checker Agent | After quiz evaluation |
| **Status** | Auto-filled by Shortlist Agent | After shortlisting |
| **Video Link** | Manual entry | When students upload videos |
| **Transcript** | Auto-filled by Video Analyzer | After video analysis |
| **Confidence** | Auto-filled by Video Analyzer | After video analysis |
| **AI Experience** | Auto-filled by Video Analyzer | After video analysis |
| **Final Result** | Auto-filled by Finalizer | After final selection |

## 🔄 **Your Workflow Will Be**

1. **Admin creates quiz questions** → Stored in your sheet
2. **Students take quiz** → Answers evaluated automatically
3. **Top 10 students shortlisted** → Status updated, emails sent
4. **Students upload videos** → Links added to sheet
5. **Videos analyzed by AI** → Transcript, confidence, AI experience filled
6. **Top 5 final selection** → Final result updated, emails sent

## 💰 **Your Estimated Costs**

- **OpenAI API**: $5-20/month (depending on video analysis volume)
- **Google Cloud**: FREE (within limits)
- **Gmail**: FREE
- **Total**: $5-20/month

## 🆘 **If You Get Stuck**

1. **Check API keys**: Make sure they're copied correctly
2. **Verify Google Sheet access**: Service account must have edit access
3. **Test Gmail**: Try sending a test email
4. **Run system test**: `python test_system.py`

Your Google Sheet structure is perfect for this system! 🎉
