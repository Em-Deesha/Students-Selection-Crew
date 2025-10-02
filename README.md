# 🎓 Student Selection Crew - AI-Powered Multi-Agent System

A comprehensive multi-agent system built with CrewAI for automated student selection processes. Features a beautiful Streamlit web interface for complete workflow management including quiz creation, evaluation, shortlisting, video analysis, and final selection.

## 🎯 System Overview

The Student Selection Crew consists of 5 specialized AI agents working together:

1. **📝 Quiz Manager** - Creates and manages quiz questions with multiple choice options
2. **🔍 Checker** - Evaluates student quiz answers automatically using AI
3. **🏆 Shortlist Agent** - Selects top 10 students and sends automated notifications
4. **🎥 Video Analyzer** - Processes video interviews using AI (OpenAI Whisper + GPT-4)
5. **🎯 Finalizer** - Makes final top 5 selection based on comprehensive analysis

## 🚀 Key Features

### 🖥️ **Beautiful Web Interface**
- **Interactive Streamlit Dashboard** - Real-time system monitoring and control
- **Responsive Design** - Works perfectly on desktop and mobile
- **Real-time Analytics** - Live charts and performance metrics
- **Modern UI** - Clean, professional interface with custom styling

### 🤖 **AI-Powered Automation**
- **Automated Quiz Evaluation** - AI-powered answer checking and scoring
- **Smart Shortlisting** - Intelligent student ranking based on performance
- **Video Analysis** - Speech-to-text transcription and AI interview analysis
- **Email Automation** - Automated notifications for each selection stage
- **Real-time Data Sync** - Live Google Sheets integration

### 📊 **Comprehensive Analytics**
- **Process Flow Visualization** - Sankey diagrams showing student progression
- **Performance Metrics** - Detailed scoring and ranking analytics
- **Success Rate Tracking** - Conversion rates at each stage
- **Export Capabilities** - Download reports and data

## 📋 Prerequisites

- Python 3.8+
- Google Cloud Platform account (for Sheets API)
- Gmail account with app password
- OpenAI API key (for video analysis)
- Google Gemini API key (optional, for enhanced AI features)

## 🛠️ Quick Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Crewai
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r frontend/requirements.txt
   ```

4. **Set up Google Sheets API:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable Google Sheets API
   - Create service account credentials
   - Download credentials JSON file
   - Share your Google Sheet with the service account email

5. **Configure environment:**
   ```bash
   cd frontend
   cp .env.example .env
   # Edit .env with your API keys and credentials
   ```

6. **Run the application:**
   ```bash
   streamlit run app.py
   ```

7. **Access the interface:**
   - Open your browser to `http://localhost:8501`

## ⚙️ Configuration

Create a `.env` file in the `frontend/` directory:

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here

# Google Services
GOOGLE_CREDENTIALS_FILE=studentcrew-473406-c69f4c709523.json
GOOGLE_SHEET_ID=your_google_sheet_id_here

# Email Configuration
GMAIL_USERNAME=your_email@gmail.com
GMAIL_APP_PASSWORD=your_app_password_here

# Project Settings
PROJECT_NAME=Student Selection Crew
MAX_SHORTLIST=10
MAX_FINAL_SELECTION=5
```

## 🎮 Using the Web Interface

### 🏠 **Dashboard**
- System overview with real-time metrics
- Recent activity timeline
- Quick action buttons
- System health monitoring

### 📝 **Quiz Manager**
- Create multiple choice questions
- Set correct answers and point values
- Organize by categories (AI/ML, Programming, etc.)
- Save directly to Google Sheets

### 📊 **Student Evaluation**
- Add student submissions manually or via CSV
- Automatic AI-powered answer evaluation
- Real-time scoring and ranking
- Visual performance charts
- Automated email notifications

### 🏆 **Shortlisting**
- View top-performing students
- Automated top 10 selection
- Send shortlist notifications
- Track student status
- Interactive ranking charts

### 🎥 **Video Analysis**
- Student video submission tracking
- AI-powered video transcription (OpenAI Whisper)
- Intelligent analysis of confidence, communication, and technical skills
- Automated scoring and evaluation
- Results integration with Google Sheets

### 🎯 **Final Selection**
- Comprehensive candidate review
- AI-assisted final top 5 selection
- Automated selection notifications
- Final reports and statistics
- Celebration animations and notifications

### 📈 **Analytics**
- Real-time process flow visualization
- Performance metrics and trends
- Success rate analysis
- Score distributions
- Comprehensive reporting

### ⚙️ **Settings**
- API configuration status
- System information
- Connection testing
- Data export capabilities

## 🚀 Complete Workflow Example

```python
# The web interface handles all of this automatically, but here's the backend flow:

from frontend.fixed_student_selection_crew import FixedStudentSelectionCrew

# Initialize the system
crew = FixedStudentSelectionCrew()

# 1. Create quiz questions (via web interface)
quiz_questions = [
    {
        'question': 'What is machine learning?',
        'options': ['AI that learns from data', 'A database', 'A language', 'Hardware'],
        'correct_answer': 0,
        'points': 2,
        'category': 'AI/ML Basics'
    }
]

# 2. Evaluate student submissions (automatic)
results = crew.evaluate_quiz_submissions(student_answers)

# 3. Shortlist top students (one-click)
shortlisted = crew.shortlist_top_students()

# 4. Analyze video interviews (AI-powered)
video_results = crew.analyze_video_interviews()

# 5. Make final selection (AI-assisted)
final_candidates = crew.make_final_selection()
```

## 📊 Data Structure

### Google Sheets Integration
The system automatically manages data in Google Sheets with these sheets:
- **Students** - Main student data and quiz scores
- **Quiz_Questions** - Question bank with answers and categories
- **Shortlisted_Students** - Top performers with video analysis
- **Quiz_Results** - Detailed evaluation results

### Student Data Format
```python
{
    'student_id': 'STU001',
    'name': 'John Doe',
    'email': 'john.doe@email.com',
    'quiz_score': '8/8 (100.0%)',
    'status': 'Shortlisted',
    'video_analysis': {
        'confidence': 8.5,
        'communication': 7.8,
        'technical': 9.2,
        'overall': 8.5
    }
}
```

## 🌐 Deployment Options

### Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your environment variables
5. Deploy with one click!

### Heroku
1. Create a `Procfile`:
   ```
   web: streamlit run frontend/app.py --server.port=$PORT --server.address=0.0.0.0
   ```
2. Deploy to Heroku with your environment variables

### Railway
1. Connect your GitHub repository
2. Railway auto-detects Streamlit apps
3. Add environment variables in dashboard
4. Deploy automatically

## 🔧 Customization

### Adding New Features
- **New Agents**: Add to `frontend/agents/` directory
- **Custom Scoring**: Modify algorithms in agent files
- **UI Components**: Add new pages to `frontend/app.py`
- **Email Templates**: Update templates in `frontend/config.py`

### Styling
- **Custom CSS**: Modify styles in `frontend/app.py`
- **Charts**: Customize Plotly visualizations
- **Themes**: Adjust color schemes and layouts

## 🐛 Troubleshooting

### Common Issues

1. **Google Sheets API Error**
   ```bash
   # Check credentials file path
   ls frontend/studentcrew-*.json
   
   # Verify sheet permissions
   # Make sure service account email has edit access
   ```

2. **Streamlit Port Issues**
   ```bash
   # Kill existing processes
   pkill -f streamlit
   
   # Run on different port
   streamlit run app.py --server.port 8502
   ```

3. **Video Analysis Failed**
   ```bash
   # Check OpenAI API key
   echo $OPENAI_API_KEY
   
   # Verify video file formats (MP4 recommended)
   ```

4. **Email Sending Failed**
   - Enable 2-factor authentication on Gmail
   - Generate app-specific password
   - Use app password in GMAIL_APP_PASSWORD

### Debug Mode
Enable verbose logging in the web interface Settings page or set:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🎯 Recent Updates (v2.0.0)

### ✨ **New Features**
- **Complete Streamlit Web Interface** - Beautiful, responsive UI
- **Real-time Analytics Dashboard** - Live charts and metrics
- **Enhanced Video Analysis** - OpenAI Whisper integration
- **Improved Email System** - Better templates and delivery
- **Google Sheets Auto-sync** - Real-time data synchronization

### 🧹 **Code Improvements**
- **Cleaned Codebase** - Removed unused imports and dead code
- **Better Error Handling** - Comprehensive try-catch blocks
- **Performance Optimization** - Faster data processing
- **Modern UI Components** - Updated Streamlit widgets

### 🔧 **Bug Fixes**
- Fixed indentation errors in crew logic
- Resolved Plotly deprecation warnings
- Improved data validation and sanitization
- Enhanced cross-platform compatibility

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly with the web interface
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- 🐛 **Issues**: Create an issue in the repository
- 📖 **Documentation**: Check the frontend/README.md for UI-specific help
- 🔧 **Troubleshooting**: Review the troubleshooting section above
- 💬 **Discussions**: Use GitHub discussions for general questions

## 🔄 Version History

- **v2.0.0** - Complete Streamlit web interface, enhanced AI features
- **v1.3.0** - Improved error handling and logging
- **v1.2.0** - Enhanced email notifications
- **v1.1.0** - Added video analysis capabilities
- **v1.0.0** - Initial release with all 5 agents

---

## 🎉 Quick Start Summary

```bash
# 1. Clone and setup
git clone <repo-url> && cd Crewai
python -m venv .venv && source .venv/bin/activate

# 2. Install and configure
pip install -r frontend/requirements.txt
cd frontend && cp .env.example .env
# Edit .env with your API keys

# 3. Run the application
streamlit run app.py

# 4. Open browser to http://localhost:8501
# 5. Start creating quizzes and selecting students! 🚀
```

**🎓 Ready to revolutionize your student selection process with AI? Get started now!**

---

**Note**: This system is designed for educational and professional use. Ensure compliance with data protection regulations when handling student information.