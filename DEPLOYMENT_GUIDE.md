# 🚀 Deployment Guide - Student Selection Crew

This guide will help you deploy your Student Selection Crew application to various cloud platforms.

## 🌟 Recommended: Streamlit Cloud (Free & Easy)

Streamlit Cloud is the easiest and free way to deploy your Streamlit application.

### 📋 Prerequisites

1. **GitHub Repository** ✅ (Already done!)
   - Your code is already pushed to: https://github.com/Em-Deesha/Students-Selection-Crew

2. **API Keys Ready** 📝
   - OpenAI API Key
   - Google Sheets API credentials
   - Gmail app password
   - Google Sheets ID

### 🚀 Step-by-Step Deployment

#### Step 1: Access Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"

#### Step 2: Connect Your Repository
1. **Repository**: `Em-Deesha/Students-Selection-Crew`
2. **Branch**: `main`
3. **Main file path**: `frontend/app.py`
4. **App URL**: Choose a custom URL (e.g., `student-selection-crew`)

#### Step 3: Configure Secrets
Click "Advanced settings" and add your secrets in the secrets management section:

```toml
# Copy and paste this template, then fill in your actual values

# API Keys
OPENAI_API_KEY = "your_actual_openai_api_key"
GOOGLE_API_KEY = "your_actual_google_api_key"
GEMINI_API_KEY = "your_actual_gemini_api_key"
ASSEMBLYAI_API_KEY = "your_actual_assemblyai_api_key"

# Google Services
GOOGLE_SHEET_ID = "your_actual_google_sheet_id"

# Email Configuration
GMAIL_USERNAME = "your_email@gmail.com"
GMAIL_APP_PASSWORD = "your_actual_app_password"

# Project Settings
PROJECT_NAME = "Student Selection Crew"
MAX_SHORTLIST = "10"
MAX_FINAL_SELECTION = "5"

# Google Service Account JSON
[google_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nyour-actual-private-key\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
```

#### Step 4: Deploy
1. Click "Deploy!"
2. Wait for the deployment to complete (usually 2-3 minutes)
3. Your app will be live at: `https://your-app-name.streamlit.app`

### 🔧 Post-Deployment Setup

1. **Test the Application**
   - Visit your deployed URL
   - Check all pages load correctly
   - Test API connections in Settings

2. **Configure Google Sheets**
   - Make sure your Google Sheet is shared with the service account email
   - Test the connection from the deployed app

3. **Verify Email System**
   - Test email sending from the Settings page
   - Ensure Gmail app password is working

## 🛠️ Alternative Deployment Options

### Option 2: Heroku

1. **Create Procfile** (already included):
   ```
   web: streamlit run frontend/app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Deploy to Heroku**:
   ```bash
   # Install Heroku CLI
   heroku create your-app-name
   heroku config:set OPENAI_API_KEY="your_key"
   heroku config:set GOOGLE_API_KEY="your_key"
   # ... add all other environment variables
   git push heroku main
   ```

### Option 3: Railway

1. **Connect Repository**
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub repository
   - Railway auto-detects Streamlit apps

2. **Add Environment Variables**
   - Add all your API keys in the Railway dashboard
   - Deploy automatically

### Option 4: Google Cloud Run

1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY frontend/ .
   RUN pip install -r requirements.txt
   
   EXPOSE 8080
   CMD streamlit run app.py --server.port=8080 --server.address=0.0.0.0
   ```

2. **Deploy**:
   ```bash
   gcloud run deploy --source . --platform managed
   ```

## 🔒 Security Best Practices

### Environment Variables
- ✅ **Never commit** `.env` files or `secrets.toml`
- ✅ **Use secrets management** in your deployment platform
- ✅ **Rotate API keys** regularly
- ✅ **Monitor usage** and costs

### Google Sheets Security
- ✅ **Service Account**: Use dedicated service account (not personal account)
- ✅ **Minimal Permissions**: Only grant necessary sheet access
- ✅ **Audit Access**: Regularly review who has access

### Email Security
- ✅ **App Passwords**: Use Gmail app passwords (not regular password)
- ✅ **2FA Required**: Enable 2-factor authentication
- ✅ **Monitor Sending**: Watch for unusual email activity

## 🐛 Troubleshooting Deployment

### Common Issues

1. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'xyz'
   ```
   **Solution**: Check `requirements.txt` includes all dependencies

2. **API Key Errors**
   ```
   Authentication failed
   ```
   **Solution**: Verify all API keys are correctly set in secrets

3. **Google Sheets Access Denied**
   ```
   403 Forbidden
   ```
   **Solution**: Ensure sheet is shared with service account email

4. **Memory/Resource Limits**
   ```
   Resource exhausted
   ```
   **Solution**: Optimize code or upgrade to paid tier

### Debug Mode

Enable debug logging by adding to your secrets:
```toml
DEBUG = "true"
```

### Health Check

Your deployed app includes a health check at `/health` endpoint.

## 📊 Monitoring Your Deployment

### Streamlit Cloud Analytics
- **Usage metrics** in Streamlit Cloud dashboard
- **Error logs** and performance monitoring
- **Resource usage** tracking

### Custom Monitoring
Add to your app:
```python
import logging
logging.basicConfig(level=logging.INFO)

# Log important events
logging.info(f"User accessed {page_name}")
logging.error(f"API error: {error_message}")
```

## 🎯 Performance Optimization

### Caching
```python
@st.cache_data
def load_data():
    # Cache expensive operations
    return data

@st.cache_resource
def init_connection():
    # Cache database connections
    return connection
```

### Resource Management
- **Optimize imports**: Only import what you need
- **Lazy loading**: Load data when needed
- **Connection pooling**: Reuse database connections

## 🔄 Continuous Deployment

### Auto-Deploy on Push
Streamlit Cloud automatically redeploys when you push to your main branch:

```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push origin main
# App automatically redeploys!
```

### Staging Environment
Create a separate branch for testing:
```bash
git checkout -b staging
# Deploy staging branch to test changes
```

## 🎉 Your App is Live!

Once deployed, your Student Selection Crew will be available at:
- **Streamlit Cloud**: `https://your-app-name.streamlit.app`
- **Custom Domain**: Configure in your deployment platform

### Share Your App
- 📱 **Mobile Friendly**: Works on all devices
- 🔗 **Direct Links**: Share specific pages
- 👥 **Multi-User**: Supports concurrent users
- 🔒 **Secure**: All credentials protected

---

## 🆘 Need Help?

- 📖 **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- 💬 **Community**: [discuss.streamlit.io](https://discuss.streamlit.io)
- 🐛 **Issues**: Create an issue in your GitHub repository
- 📧 **Support**: Check platform-specific documentation

**🚀 Ready to deploy? Follow the Streamlit Cloud steps above and your AI-powered student selection system will be live in minutes!**
