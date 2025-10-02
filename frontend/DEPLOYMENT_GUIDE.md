# 🚀 Deployment Guide - Student Selection Crew Frontend

## 🌐 Free Deployment Options

### Option 1: Streamlit Cloud (Recommended - 100% Free)

**Steps:**
1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/student-selection-crew.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Choose `frontend/demo_app.py` as the main file
   - Click "Deploy"

3. **Your app will be live at:** `https://your-app-name.streamlit.app`

### Option 2: Railway (Free Tier)

**Steps:**
1. **Create railway.json:**
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "streamlit run demo_app.py --server.port $PORT --server.address 0.0.0.0"
     }
   }
   ```

2. **Deploy:**
   - Go to [railway.app](https://railway.app)
   - Connect GitHub repository
   - Railway auto-detects and deploys
   - Add environment variables if needed

### Option 3: Heroku (Free Tier - Limited)

**Steps:**
1. **Create Procfile:**
   ```
   web: streamlit run demo_app.py --server.port $PORT --server.address 0.0.0.0
   ```

2. **Deploy:**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Option 4: Render (Free Tier)

**Steps:**
1. **Create render.yaml:**
   ```yaml
   services:
     - type: web
       name: student-selection-crew
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: streamlit run demo_app.py --server.port $PORT --server.address 0.0.0.0
   ```

2. **Deploy:**
   - Connect GitHub repository
   - Render auto-detects and deploys

## 🔧 Environment Variables

For production deployment, set these environment variables:

```bash
# API Keys
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
GEMINI_API_KEY=your_gemini_key
ASSEMBLYAI_API_KEY=your_assemblyai_key

# Google Services
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_ID=your_sheet_id
GOOGLE_DRIVE_FOLDER_ID=your_drive_folder_id

# Email
GMAIL_USERNAME=your_email@gmail.com
GMAIL_APP_PASSWORD=your_app_password

# Settings
PROJECT_NAME=Student Selection Crew
MAX_SHORTLIST=10
MAX_FINAL_SELECTION=5
```

## 📱 Features Overview

### 🏠 Dashboard
- Real-time system metrics
- Activity timeline
- System health status
- Performance charts

### 📝 Quiz Manager
- Create quiz questions
- Multiple choice options
- Point values and categories
- Save to Google Sheets

### 📊 Student Evaluation
- Add student submissions
- Automatic scoring
- Performance visualization
- Export results

### 🏆 Shortlisting
- Select top students
- Email notifications
- Ranking visualization
- Status tracking

### 🎥 Video Analysis
- Upload video files
- AI-powered analysis
- Confidence scoring
- Experience evaluation

### 🎯 Final Selection
- Review all data
- Make final decisions
- Send notifications
- Generate reports

### 📈 Analytics
- Process flow diagrams
- Performance trends
- Success metrics
- Custom reports

### ⚙️ Settings
- API configuration
- System information
- Connection testing
- Data export

## 🎨 Customization

### Colors and Themes
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### Custom CSS
Modify the CSS in `app.py` or `demo_app.py` to match your brand.

## 🔒 Security Considerations

1. **Environment Variables:** Never commit API keys to GitHub
2. **Credentials:** Store sensitive data in environment variables
3. **Access Control:** Consider adding authentication for production
4. **Rate Limiting:** Implement rate limiting for API calls

## 📊 Monitoring

### Streamlit Cloud
- Built-in analytics
- Usage statistics
- Error monitoring

### Custom Monitoring
- Add logging to track usage
- Monitor API calls
- Set up alerts for errors

## 🚀 Quick Start Commands

```bash
# Local development
streamlit run demo_app.py

# Production deployment
streamlit run app.py --server.port $PORT --server.address 0.0.0.0

# With custom config
streamlit run demo_app.py --server.port 8501 --server.headless true
```

## 🆘 Troubleshooting

### Common Issues:
1. **Port conflicts:** Change port in command
2. **Dependencies:** Check requirements.txt
3. **Environment variables:** Verify all are set
4. **API limits:** Check rate limits

### Debug Mode:
```bash
streamlit run demo_app.py --logger.level debug
```

## 📞 Support

- Check the main README.md
- Review setup guides
- Test API connections
- Check deployment logs

Your beautiful Student Selection Crew interface is ready for deployment! 🎉
