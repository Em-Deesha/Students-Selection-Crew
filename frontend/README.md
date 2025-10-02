# 🎓 Student Selection Crew - Frontend

A beautiful and interactive web interface for your Student Selection Crew multi-agent system.

## 🚀 Features

- **📊 Interactive Dashboard** - Real-time system status and analytics
- **📝 Quiz Manager** - Create and manage quiz questions
- **📊 Student Evaluation** - Evaluate student submissions with visual results
- **🏆 Shortlisting** - Select top students with automated notifications
- **🎥 Video Analysis** - Upload and analyze video interviews
- **🎯 Final Selection** - Make final candidate selections
- **📈 Analytics** - Comprehensive reports and visualizations
- **⚙️ Settings** - System configuration and management

## 🛠️ Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   streamlit run app.py
   ```

3. **Access the interface:**
   - Open your browser to `http://localhost:8501`

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Free)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click!

### Option 2: Heroku (Free Tier)
1. Create a `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Deploy to Heroku:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Option 3: Railway (Free Tier)
1. Connect your GitHub repository
2. Railway will automatically detect and deploy
3. Add environment variables in Railway dashboard

## 📱 Interface Overview

### 🏠 Dashboard
- System overview with key metrics
- Recent activity timeline
- System health status
- Performance charts

### 📝 Quiz Manager
- Create quiz questions with multiple choice options
- Set correct answers and point values
- Organize by categories
- Save to Google Sheets

### 📊 Student Evaluation
- Add student submissions
- Automatic answer evaluation
- Visual performance charts
- Export results

### 🏆 Shortlisting
- Select top performing students
- Send email notifications
- Track shortlist status
- Generate reports

### 🎥 Video Analysis
- Upload video files
- AI-powered analysis
- Confidence scoring
- Experience evaluation

### 🎯 Final Selection
- Review all candidate data
- Make final selections
- Send selection notifications
- Generate final reports

### 📈 Analytics
- Process flow visualization
- Performance trends
- Success metrics
- Custom reports

### ⚙️ Settings
- API configuration status
- System information
- Connection testing
- Data export

## 🎨 Customization

The interface is built with Streamlit and includes:
- Custom CSS styling
- Interactive charts with Plotly
- Responsive design
- Modern UI components

## 🔧 Configuration

Make sure your backend system is properly configured:
- Google Sheets API
- Gmail credentials
- OpenAI API key
- All environment variables

## 📞 Support

For issues or questions:
1. Check the main README.md
2. Review the setup guides
3. Test your API connections
4. Check the logs for errors

## 🚀 Quick Start

1. **Clone the repository**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Configure your APIs** (see main README)
4. **Run the app**: `streamlit run app.py`
5. **Deploy to cloud** (optional)

Your beautiful Student Selection Crew interface is ready! 🎉
