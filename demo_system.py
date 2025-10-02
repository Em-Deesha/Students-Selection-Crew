"""
Demo script to show your Student Selection Crew in action
"""
from student_selection_crew import StudentSelectionCrew
from config import Config
import os

def demo_quiz_creation():
    """Demo: Create sample quiz questions"""
    print("🎯 DEMO: Creating Quiz Questions")
    print("=" * 40)
    
    # Sample quiz questions
    quiz_questions = [
        {
            'question': 'What is machine learning?',
            'options': [
                'A computer program that learns from data',
                'A type of database',
                'A programming language',
                'A hardware component'
            ],
            'correct_answer': 0,
            'points': 2,
            'category': 'AI/ML Basics'
        },
        {
            'question': 'Which algorithm is commonly used for classification?',
            'options': [
                'Linear Regression',
                'Random Forest',
                'K-means',
                'A* Search'
            ],
            'correct_answer': 1,
            'points': 2,
            'category': 'Algorithms'
        },
        {
            'question': 'What is the purpose of cross-validation?',
            'options': [
                'To increase model complexity',
                'To evaluate model performance',
                'To reduce data size',
                'To speed up training'
            ],
            'correct_answer': 1,
            'points': 3,
            'category': 'Model Evaluation'
        }
    ]
    
    print(f"Created {len(quiz_questions)} quiz questions:")
    for i, q in enumerate(quiz_questions, 1):
        print(f"  {i}. {q['question']} ({q['category']})")
    
    return quiz_questions

def demo_student_answers():
    """Demo: Sample student answers"""
    print("\n👥 DEMO: Student Quiz Submissions")
    print("=" * 40)
    
    student_answers = [
        {
            'student_id': 'STU001',
            'name': 'John Doe',
            'email': 'john.doe@email.com',
            'answers': [0, 1, 1]  # Answers to the 3 questions
        },
        {
            'student_id': 'STU002',
            'name': 'Jane Smith',
            'email': 'jane.smith@email.com',
            'answers': [0, 1, 0]
        },
        {
            'student_id': 'STU003',
            'name': 'Bob Johnson',
            'email': 'bob.johnson@email.com',
            'answers': [1, 0, 1]
        },
        {
            'student_id': 'STU004',
            'name': 'Alice Brown',
            'email': 'alice.brown@email.com',
            'answers': [0, 1, 1]
        },
        {
            'student_id': 'STU005',
            'name': 'Charlie Wilson',
            'email': 'charlie.wilson@email.com',
            'answers': [0, 0, 0]
        }
    ]
    
    print(f"Received {len(student_answers)} student submissions:")
    for student in student_answers:
        print(f"  {student['student_id']}: {student['name']} ({student['email']})")
    
    return student_answers

def demo_video_data():
    """Demo: Sample video interview data"""
    print("\n🎥 DEMO: Video Interview Data")
    print("=" * 40)
    
    video_data = [
        {
            'student_id': 'STU001',
            'video_path': '/path/to/john_doe_interview.mp4'
        },
        {
            'student_id': 'STU002',
            'video_path': '/path/to/jane_smith_interview.mp4'
        },
        {
            'student_id': 'STU003',
            'video_path': '/path/to/bob_johnson_interview.mp4'
        }
    ]
    
    print(f"Received {len(video_data)} video interviews:")
    for video in video_data:
        print(f"  {video['student_id']}: {video['video_path']}")
    
    return video_data

def main():
    """Run the complete demo"""
    print("🚀 STUDENT SELECTION CREW - LIVE DEMO")
    print("=" * 50)
    print("This demo shows how your multi-agent system works!")
    print()
    
    # Initialize the crew (this will test all connections)
    print("🔧 Initializing Student Selection Crew...")
    try:
        crew = StudentSelectionCrew(
            credentials_file=Config.GOOGLE_CREDENTIALS_FILE,
            sheet_id=Config.GOOGLE_SHEET_ID,
            gmail_username=Config.GMAIL_USERNAME,
            gmail_password=Config.GMAIL_APP_PASSWORD
        )
        print("✅ Crew initialized successfully!")
    except Exception as e:
        print(f"❌ Crew initialization failed: {e}")
        print("Please check your API configuration.")
        return
    
    # Demo 1: Quiz Creation
    quiz_questions = demo_quiz_creation()
    
    # Demo 2: Student Answers
    student_answers = demo_student_answers()
    
    # Demo 3: Video Data
    video_data = demo_video_data()
    
    print("\n🔄 DEMO: Complete Workflow")
    print("=" * 40)
    print("Your system would now:")
    print("1. ✅ Store quiz questions in Google Sheets")
    print("2. ✅ Evaluate student answers automatically")
    print("3. ✅ Shortlist top 10 students")
    print("4. ✅ Send email notifications to shortlisted students")
    print("5. ✅ Analyze video interviews with AI")
    print("6. ✅ Select final top 5 candidates")
    print("7. ✅ Send final selection emails")
    
    print("\n📊 DEMO: System Status")
    print("=" * 40)
    try:
        status = crew.get_process_status()
        print(f"Quiz questions: {status['quiz_questions']}")
        print(f"Quiz results: {status['quiz_results']}")
        print(f"Shortlisted: {status['shortlisted']}")
        print(f"Video analysis: {status['video_analysis']}")
        print(f"Final selection: {status['final_selection']}")
    except Exception as e:
        print(f"Status check failed: {e}")
    
    print("\n🎉 DEMO COMPLETE!")
    print("=" * 50)
    print("Your Student Selection Crew is ready for real use!")
    print("\nTo start using the system:")
    print("1. Create your quiz questions")
    print("2. Have students take the quiz")
    print("3. Run the evaluation process")
    print("4. Shortlist top students")
    print("5. Analyze video interviews")
    print("6. Make final selections")
    
    print("\n📚 Documentation:")
    print("- README.md: Complete system documentation")
    print("- setup_guide.md: Step-by-step setup")
    print("- API_SETUP_GUIDE.md: API configuration guide")

if __name__ == "__main__":
    main()
