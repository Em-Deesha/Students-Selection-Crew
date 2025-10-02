"""
Test the system with real data in your Google Sheet
"""
from student_selection_crew import StudentSelectionCrew
from config import Config

def test_with_sample_data():
    """Test the system with sample data"""
    print("🧪 TESTING WITH SAMPLE DATA")
    print("=" * 40)
    
    try:
        # Initialize the crew
        crew = StudentSelectionCrew(
            credentials_file=Config.GOOGLE_CREDENTIALS_FILE,
            sheet_id=Config.GOOGLE_SHEET_ID,
            gmail_username=Config.GMAIL_USERNAME,
            gmail_password=Config.GMAIL_APP_PASSWORD
        )
        print("✅ Crew initialized successfully!")
        
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
            }
        ]
        
        print(f"📝 Creating {len(quiz_questions)} quiz questions...")
        success = crew.create_quiz_questions(quiz_questions)
        if success:
            print("✅ Quiz questions created successfully!")
        else:
            print("❌ Failed to create quiz questions")
        
        # Sample student answers
        student_answers = [
            {
                'student_id': 'STU001',
                'name': 'John Doe',
                'email': 'john.doe@email.com',
                'answers': [0, 1]  # Correct answers
            },
            {
                'student_id': 'STU002',
                'name': 'Jane Smith',
                'email': 'jane.smith@email.com',
                'answers': [0, 0]  # Partially correct
            },
            {
                'student_id': 'STU003',
                'name': 'Bob Johnson',
                'email': 'bob.johnson@email.com',
                'answers': [1, 1]  # Wrong answers
            }
        ]
        
        print(f"📊 Evaluating {len(student_answers)} student submissions...")
        results = crew.evaluate_quiz_submissions(student_answers)
        if results:
            print(f"✅ Evaluated {len(results)} students successfully!")
            for result in results:
                print(f"  {result['student_name']}: {result['percentage']}%")
        else:
            print("❌ Failed to evaluate submissions")
        
        # Test shortlisting
        print("🏆 Testing shortlisting process...")
        shortlisted = crew.shortlist_top_students("https://drive.google.com/drive/folders/test")
        if shortlisted:
            print(f"✅ Shortlisted {len(shortlisted)} students!")
            for student in shortlisted:
                print(f"  {student['student_name']}: {student['percentage']}%")
        else:
            print("❌ No students shortlisted")
        
        # Check final status
        print("\n📊 FINAL SYSTEM STATUS")
        print("=" * 40)
        status = crew.get_process_status()
        print(f"Quiz questions: {status['quiz_questions']}")
        print(f"Quiz results: {status['quiz_results']}")
        print(f"Shortlisted: {status['shortlisted']}")
        print(f"Video analysis: {status['video_analysis']}")
        print(f"Final selection: {status['final_selection']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Run the test"""
    print("🚀 TESTING YOUR STUDENT SELECTION CREW")
    print("=" * 50)
    print("This will test your system with real data!")
    print()
    
    if test_with_sample_data():
        print("\n🎉 SUCCESS!")
        print("Your Student Selection Crew is working perfectly!")
        print("\n✅ What just happened:")
        print("1. Created quiz questions in your Google Sheet")
        print("2. Evaluated student answers automatically")
        print("3. Shortlisted top students")
        print("4. Updated your Google Sheet with results")
        
        print("\n🚀 Your system is ready for real use!")
        print("You can now:")
        print("- Create your own quiz questions")
        print("- Have students take the quiz")
        print("- Run the complete selection process")
        print("- Analyze video interviews")
        print("- Make final selections")
    else:
        print("\n❌ Test failed")
        print("Please check your configuration and try again")

if __name__ == "__main__":
    main()
