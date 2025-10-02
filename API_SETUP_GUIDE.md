# 🔑 API Setup Guide for Student Selection Crew

## 📋 Required APIs and Setup Instructions

Based on your Google Sheet: `https://docs.google.com/spreadsheets/d/1UoGodmpxsuAUB9BzL7ILYWWNRw5tOiqKnAkxdvl6Wm8/edit`

### 🎯 **REQUIRED APIs** (Must Have)

#### 1. **OpenAI API** ⭐ **CRITICAL**
- **Purpose**: AI analysis of video transcripts and content
- **Get it from**: https://platform.openai.com/api-keys
- **Cost**: ~$5-20/month depending on usage
- **Steps**:
  1. Go to https://platform.openai.com/
  2. Sign up/Login
  3. Go to "API Keys" section
  4. Click "Create new secret key"
  5. Copy the key (starts with `sk-`)
  6. Add to `.env`: `OPENAI_API_KEY=sk-your-key-here`

#### 2. **Google Cloud APIs** ⭐ **CRITICAL**
- **Purpose**: Google Sheets access, Gmail sending
- **Get it from**: https://console.cloud.google.com/
- **Cost**: FREE (with limits)
- **Steps**:
  1. Go to https://console.cloud.google.com/
  2. Create new project: "Student Selection Crew"
  3. Enable APIs:
     - Google Sheets API
     - Gmail API
     - Google Drive API (optional)
  4. Create Service Account:
     - Go to "Credentials" → "Create Credentials" → "Service Account"
     - Name: "student-selection-service"
     - Download JSON key file → rename to `credentials.json`
  5. Share your Google Sheet with the service account email
  6. Get API key from "Credentials" → "Create Credentials" → "API Key"
  7. Add to `.env`: `GOOGLE_API_KEY=your-google-api-key`

#### 3. **Gmail App Password** ⭐ **CRITICAL**
- **Purpose**: Sending emails to students
- **Get it from**: Your Google Account settings
- **Cost**: FREE
- **Steps**:
  1. Go to https://myaccount.google.com/
  2. Security → 2-Step Verification (enable if not already)
  3. Security → App passwords
  4. Select "Mail" → "Other" → Name: "Student Selection Crew"
  5. Copy the 16-character password
  6. Add to `.env`: `GMAIL_APP_PASSWORD=your-16-char-password`

### 🔧 **OPTIONAL APIs** (Nice to Have)

#### 4. **Google Gemini API** (Optional)
- **Purpose**: Alternative AI for video analysis
- **Get it from**: https://makersuite.google.com/app/apikey
- **Cost**: FREE (with limits)
- **Steps**:
  1. Go to https://makersuite.google.com/
  2. Click "Get API key"
  3. Create new API key
  4. Copy the key
  5. Add to `.env`: `GEMINI_API_KEY=your-gemini-key`

#### 5. **AssemblyAI API** (Optional)
- **Purpose**: High-quality speech-to-text for videos
- **Get it from**: https://www.assemblyai.com/dashboard/signup
- **Cost**: FREE tier available
- **Steps**:
  1. Sign up at https://www.assemblyai.com/
  2. Go to Dashboard → API Key
  3. Copy the key
  4. Add to `.env`: `ASSEMBLYAI_API_KEY=your-assemblyai-key`

## 📊 **Your Google Sheet Structure**

Your sheet has the perfect structure for our system:
```
Student Name | Email | Quiz Marks | Status | Video Link | Transcript | Confidence | AI Experience | Final Result
```

This matches exactly what our system needs! 🎉

## 🚀 **Quick Setup Checklist**

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Up APIs (Minimum Required)
- [ ] Get OpenAI API key
- [ ] Set up Google Cloud project
- [ ] Create service account
- [ ] Download credentials.json
- [ ] Share Google Sheet with service account
- [ ] Get Gmail app password

### Step 3: Update .env File
```bash
# Edit your .env file with real values:
OPENAI_API_KEY=sk-your-real-key-here
GOOGLE_API_KEY=your-real-google-key-here
GMAIL_USERNAME=your-real-email@gmail.com
GMAIL_APP_PASSWORD=your-real-16-char-password
```

### Step 4: Test the System
```bash
python test_system.py
```

## 💰 **Cost Breakdown**

| API | Cost | Usage |
|-----|------|-------|
| OpenAI | $5-20/month | Video analysis, content generation |
| Google Cloud | FREE | Sheets access, Gmail sending |
| Gmail | FREE | Email notifications |
| Gemini (Optional) | FREE | Alternative AI analysis |
| AssemblyAI (Optional) | FREE tier | High-quality speech-to-text |

**Total Estimated Cost: $5-20/month**

## 🔧 **Your Specific Configuration**

Based on your Google Sheet, here's what you need to update in `.env`:

```env
# Your specific Google Sheet ID
GOOGLE_SHEET_ID=1UoGodmpxsuAUB9BzL7ILYWWNRw5tOiqKnAkxdvl6Wm8

# Your email (replace with your actual email)
GMAIL_USERNAME=your-email@gmail.com

# Your Gmail app password (16 characters)
GMAIL_APP_PASSWORD=your-app-password-here

# Your OpenAI API key
OPENAI_API_KEY=sk-your-openai-key-here

# Your Google API key
GOOGLE_API_KEY=your-google-api-key-here
```

## 🎯 **Next Steps After API Setup**

1. **Test the system**: `python test_system.py`
2. **Run example**: `python example_usage.py`
3. **Create your first quiz**: Use the quiz manager
4. **Start the selection process**: Follow the workflow

## 🆘 **Troubleshooting**

### Common Issues:
- **"Invalid API key"**: Check if you copied the key correctly
- **"Sheet not accessible"**: Ensure service account has access
- **"Email failed"**: Check Gmail app password
- **"Video analysis failed"**: Install FFmpeg: `sudo apt-get install ffmpeg`

### Need Help?
- Check the main README.md
- Review setup_guide.md
- Test each component individually

Your Google Sheet structure is perfect for this system! 🎉
