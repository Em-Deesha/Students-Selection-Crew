"""
Student Selection Crew - Demo Frontend
A beautiful demo interface that works without the full backend
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="Student Selection Crew - Demo",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .info-box {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def display_header():
    """Display the main header"""
    st.markdown('<h1 class="main-header">🎓 Student Selection Crew</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem; color: #666;">
            AI-Powered Multi-Agent System for Automated Student Selection
        </p>
        <div class="info-box">
            <strong>🎯 Demo Mode:</strong> This is a demonstration of the full system interface. 
            Connect your backend to enable all features!
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_sidebar():
    """Display sidebar with navigation"""
    st.sidebar.title("🎯 Navigation")
    
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["🏠 Dashboard", "📝 Quiz Manager", "📊 Student Evaluation", "🏆 Shortlisting", 
         "🎥 Video Analysis", "🎯 Final Selection", "📈 Analytics", "⚙️ Settings"]
    )
    
    st.sidebar.markdown("---")
    
    # Demo Status
    st.sidebar.title("📊 Demo Status")
    st.sidebar.metric("Quiz Questions", "3")
    st.sidebar.metric("Students Evaluated", "15")
    st.sidebar.metric("Shortlisted", "10")
    st.sidebar.metric("Video Analysis", "8")
    st.sidebar.metric("Final Selection", "5")
    
    st.sidebar.markdown("---")
    
    # Quick Actions
    st.sidebar.title("🚀 Quick Actions")
    if st.sidebar.button("🔄 Refresh Demo"):
        st.rerun()
    
    st.sidebar.markdown("""
    **🔗 Connect Backend:**
    - Configure APIs
    - Set up Google Sheets
    - Enable email notifications
    - Activate AI analysis
    """)
    
    return page

def dashboard_page():
    """Display the main dashboard"""
    st.title("🏠 Dashboard")
    
    # System Overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📝 Quiz Questions</h3>
            <h2>3</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>👥 Students</h3>
            <h2>15</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🏆 Shortlisted</h3>
            <h2>10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Final Selection</h3>
            <h2>5</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent Activity
    st.subheader("📈 Recent Activity")
    
    activity_data = pd.DataFrame({
        'Time': ['10:30 AM', '10:15 AM', '10:00 AM', '9:45 AM', '9:30 AM'],
        'Activity': [
            'Final selection completed',
            'Video analysis finished',
            'Students shortlisted',
            'Quiz evaluation completed',
            'Quiz questions created'
        ],
        'Status': ['✅', '✅', '✅', '✅', '✅']
    })
    
    st.dataframe(activity_data, use_container_width=True)
    
    # System Health
    st.subheader("🔧 System Health")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **✅ All Systems Operational**
        - Google Sheets: Connected
        - Email Service: Active
        - AI Services: Ready
        - Video Analysis: Available
        """)
    
    with col2:
        # Sample chart
        fig = go.Figure(data=go.Scatter(
            x=['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            y=[5, 8, 12, 15],
            mode='lines+markers',
            name='Applications'
        ))
        fig.update_layout(title="Applications Over Time", height=300)
        st.plotly_chart(fig, use_container_width=True)

def quiz_manager_page():
    """Display quiz management page"""
    st.title("📝 Quiz Manager")
    
    st.subheader("➕ Create New Quiz Questions")
    
    with st.form("quiz_form"):
        question = st.text_area("Question:", placeholder="Enter your question here...")
        
        col1, col2 = st.columns(2)
        with col1:
            option_a = st.text_input("Option A:", placeholder="First option")
            option_c = st.text_input("Option C:", placeholder="Third option")
        with col2:
            option_b = st.text_input("Option B:", placeholder="Second option")
            option_d = st.text_input("Option D:", placeholder="Fourth option")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            correct_answer = st.selectbox("Correct Answer:", [0, 1, 2, 3], format_func=lambda x: f"Option {chr(65+x)}")
        with col2:
            points = st.number_input("Points:", min_value=1, max_value=10, value=2)
        with col3:
            category = st.text_input("Category:", placeholder="e.g., AI/ML Basics")
        
        submitted = st.form_submit_button("➕ Add Question")
        
        if submitted and question and option_a and option_b:
            st.success("✅ Question added successfully!")
    
    # Sample questions
    st.subheader("📋 Sample Quiz Questions")
    
    sample_questions = [
        {
            'question': 'What is machine learning?',
            'options': ['A computer program that learns from data', 'A type of database', 'A programming language', 'A hardware component'],
            'correct': 'A',
            'points': 2,
            'category': 'AI/ML Basics'
        },
        {
            'question': 'Which algorithm is commonly used for classification?',
            'options': ['Linear Regression', 'Random Forest', 'K-means', 'A* Search'],
            'correct': 'B',
            'points': 2,
            'category': 'Algorithms'
        },
        {
            'question': 'What is the purpose of cross-validation?',
            'options': ['To increase model complexity', 'To evaluate model performance', 'To reduce data size', 'To speed up training'],
            'correct': 'B',
            'points': 3,
            'category': 'Model Evaluation'
        }
    ]
    
    for i, q in enumerate(sample_questions):
        with st.expander(f"Question {i+1}: {q['question']}"):
            st.write(f"**Question:** {q['question']}")
            st.write(f"**Options:**")
            for j, option in enumerate(q['options']):
                st.write(f"  {chr(65+j)}. {option}")
            st.write(f"**Correct Answer:** Option {q['correct']}")
            st.write(f"**Points:** {q['points']}")
            st.write(f"**Category:** {q['category']}")

def student_evaluation_page():
    """Display student evaluation page"""
    st.title("📊 Student Evaluation")
    
    st.subheader("👥 Student Submissions")
    
    # Sample student data
    students_data = pd.DataFrame({
        'Student ID': ['STU001', 'STU002', 'STU003', 'STU004', 'STU005'],
        'Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson'],
        'Email': ['john@email.com', 'jane@email.com', 'bob@email.com', 'alice@email.com', 'charlie@email.com'],
        'Quiz Score': [100, 85, 70, 95, 60],
        'Percentage': [100.0, 85.0, 70.0, 95.0, 60.0],
        'Status': ['Completed', 'Completed', 'Completed', 'Completed', 'Completed']
    })
    
    st.dataframe(students_data, use_container_width=True)
    
    # Performance visualization
    st.subheader("📈 Performance Analysis")
    
    fig = px.bar(students_data, x='Name', y='Percentage', 
                 title="Student Performance", color='Percentage',
                 color_continuous_scale='RdYlGn')
    st.plotly_chart(fig, use_container_width=True)
    
    # Add new student
    st.subheader("➕ Add New Student")
    
    with st.form("student_form"):
        col1, col2 = st.columns(2)
        with col1:
            student_name = st.text_input("Student Name:", placeholder="Enter student name")
            student_email = st.text_input("Email:", placeholder="Enter email address")
        with col2:
            student_id = st.text_input("Student ID:", placeholder="Enter student ID")
        
        submitted = st.form_submit_button("➕ Add Student")
        
        if submitted and student_name and student_email:
            st.success("✅ Student added successfully!")

def shortlisting_page():
    """Display shortlisting page"""
    st.title("🏆 Student Shortlisting")
    
    st.subheader("🎯 Shortlisted Students")
    
    # Sample shortlisted students
    shortlisted_data = pd.DataFrame({
        'Student ID': ['STU001', 'STU004', 'STU002', 'STU003', 'STU005'],
        'Name': ['John Doe', 'Alice Brown', 'Jane Smith', 'Bob Johnson', 'Charlie Wilson'],
        'Email': ['john@email.com', 'alice@email.com', 'jane@email.com', 'bob@email.com', 'charlie@email.com'],
        'Quiz Score': [100, 95, 85, 70, 60],
        'Rank': [1, 2, 3, 4, 5],
        'Status': ['Shortlisted', 'Shortlisted', 'Shortlisted', 'Shortlisted', 'Shortlisted']
    })
    
    st.dataframe(shortlisted_data, use_container_width=True)
    
    # Ranking chart
    fig = px.bar(shortlisted_data, x='Name', y='Quiz Score',
                 title="Shortlisted Students Ranking",
                 color='Quiz Score', color_continuous_scale='viridis')
    st.plotly_chart(fig, use_container_width=True)
    
    # Shortlisting controls
    st.subheader("🎯 Shortlisting Controls")
    
    col1, col2 = st.columns(2)
    with col1:
        drive_link = st.text_input("Google Drive Link:", 
                                 placeholder="https://drive.google.com/drive/folders/...")
    with col2:
        deadline = st.date_input("Submission Deadline:", 
                               value=datetime.now() + timedelta(days=7))
    
    if st.button("🏆 Start Shortlisting Process"):
        if drive_link:
            st.success("✅ Shortlisting process started!")
            st.info("📧 Email notifications sent to shortlisted students")
        else:
            st.error("❌ Please provide a Google Drive link")

def video_analysis_page():
    """Display video analysis page"""
    st.title("🎥 Video Analysis")
    
    st.subheader("📹 Video Analysis Results")
    
    # Sample video analysis data
    video_data = pd.DataFrame({
        'Student ID': ['STU001', 'STU002', 'STU003', 'STU004'],
        'Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown'],
        'Video File': ['john_interview.mp4', 'jane_interview.mp4', 'bob_interview.mp4', 'alice_interview.mp4'],
        'Confidence Score': [8.5, 7.2, 6.8, 9.1],
        'AI Experience': [7.5, 6.0, 5.5, 8.0],
        'Education Status': ['Graduated', 'Final Year', 'Graduated', 'Final Year'],
        'Transcript': ['Sample transcript...', 'Sample transcript...', 'Sample transcript...', 'Sample transcript...']
    })
    
    st.dataframe(video_data, use_container_width=True)
    
    # Analysis charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(video_data, x='Name', y='Confidence Score',
                      title="Confidence Scores", color='Confidence Score',
                      color_continuous_scale='RdYlGn')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.bar(video_data, x='Name', y='AI Experience',
                      title="AI Experience Scores", color='AI Experience',
                      color_continuous_scale='Blues')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Upload new videos
    st.subheader("📤 Upload New Videos")
    
    uploaded_files = st.file_uploader("Choose video files", 
                                    accept_multiple_files=True, 
                                    type=['mp4', 'avi', 'mov'])
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} video files uploaded!")
        
        if st.button("🔍 Analyze Videos"):
            with st.spinner("Analyzing videos..."):
                st.success("✅ Video analysis completed!")

def final_selection_page():
    """Display final selection page"""
    st.title("🎯 Final Selection")
    
    st.subheader("🏆 Final Selected Candidates")
    
    # Sample final candidates
    final_data = pd.DataFrame({
        'Student ID': ['STU001', 'STU004', 'STU002'],
        'Name': ['John Doe', 'Alice Brown', 'Jane Smith'],
        'Email': ['john@email.com', 'alice@email.com', 'jane@email.com'],
        'Quiz Score': [100, 95, 85],
        'Confidence': [8.5, 9.1, 7.2],
        'AI Experience': [7.5, 8.0, 6.0],
        'Comprehensive Score': [8.7, 8.8, 7.1],
        'Status': ['Selected', 'Selected', 'Selected']
    })
    
    st.dataframe(final_data, use_container_width=True)
    
    # Final selection chart
    fig = px.bar(final_data, x='Name', y='Comprehensive Score',
                 title="Final Selection Results",
                 color='Comprehensive Score',
                 color_continuous_scale='viridis')
    st.plotly_chart(fig, use_container_width=True)
    
    # Selection controls
    st.subheader("🎯 Final Selection Controls")
    
    if st.button("🎯 Send Final Notifications"):
        st.success("✅ Final selection notifications sent!")
        st.info("📧 Email notifications sent to selected candidates")

def analytics_page():
    """Display analytics page"""
    st.title("📈 Analytics & Reports")
    
    # Process flow chart
    st.subheader("📊 Selection Process Flow")
    
    fig = go.Figure(data=go.Sankey(
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = ["Applications", "Quiz Taken", "Shortlisted", "Video Submitted", "Final Selection"],
            color = ["blue", "green", "orange", "purple", "red"]
        ),
        link = dict(
            source = [0, 1, 2, 3],
            target = [1, 2, 3, 4],
            value = [100, 80, 20, 5]
        )
    ))
    
    fig.update_layout(title_text="Selection Process Flow", font_size=10)
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Performance Trends")
        
        trend_data = pd.DataFrame({
            'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            'Applications': [20, 35, 50, 65],
            'Shortlisted': [15, 25, 35, 45],
            'Selected': [5, 8, 12, 15]
        })
        
        fig = px.line(trend_data, x='Week', y=['Applications', 'Shortlisted', 'Selected'],
                     title="Weekly Performance Trends")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Success Metrics")
        
        metrics_data = pd.DataFrame({
            'Metric': ['Conversion Rate', 'Completion Rate', 'Satisfaction Score'],
            'Value': [23.1, 87.5, 4.2],
            'Target': [20.0, 85.0, 4.0]
        })
        
        fig = px.bar(metrics_data, x='Metric', y='Value',
                    title="Key Performance Indicators",
                    color='Value', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)

def settings_page():
    """Display settings page"""
    st.title("⚙️ Settings")
    
    st.subheader("🔧 System Configuration")
    
    # API Status
    st.write("**API Configuration Status:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("✅ OpenAI API: Configured")
        st.success("✅ Google Sheets: Connected")
        st.success("✅ Gmail: Active")
    
    with col2:
        st.success("✅ Gemini API: Configured")
        st.success("✅ AssemblyAI: Available")
        st.info("ℹ️ Video Analysis: Ready")
    
    st.subheader("📊 System Information")
    
    info_data = {
        'Component': ['Google Sheet ID', 'Gmail Username', 'Max Shortlist', 'Max Final Selection'],
        'Value': ['1UoGodmpxsuAUB9BzL7ILYWWNRw5tOiqKnAkxdvl6Wm8', 'your-email@gmail.com', '10', '5']
    }
    
    st.dataframe(pd.DataFrame(info_data), use_container_width=True)
    
    st.subheader("🔄 System Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh System"):
            st.rerun()
    
    with col2:
        if st.button("📊 Test Connections"):
            st.info("Testing all API connections...")
            st.success("✅ All connections successful!")
    
    with col3:
        if st.button("📋 Export Data"):
            st.info("Exporting system data...")
            st.success("✅ Data exported successfully!")

def main():
    """Main application function"""
    display_header()
    
    # Sidebar navigation
    page = display_sidebar()
    
    # Route to appropriate page
    if page == "🏠 Dashboard":
        dashboard_page()
    elif page == "📝 Quiz Manager":
        quiz_manager_page()
    elif page == "📊 Student Evaluation":
        student_evaluation_page()
    elif page == "🏆 Shortlisting":
        shortlisting_page()
    elif page == "🎥 Video Analysis":
        video_analysis_page()
    elif page == "🎯 Final Selection":
        final_selection_page()
    elif page == "📈 Analytics":
        analytics_page()
    elif page == "⚙️ Settings":
        settings_page()

if __name__ == "__main__":
    main()
