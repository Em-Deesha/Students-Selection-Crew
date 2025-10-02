"""
Example usage of the Student Selection Crew
"""
import os
from student_selection_crew import StudentSelectionCrew
from config import Config

def main():
    """
    Example of how to use the Student Selection Crew
    """
    
    # Configuration (you'll need to set these up)
    credentials_file = "credentials.json"  # Google service account credentials
    sheet_id = "your_google_sheet_id_here"
    gmail_username = "your_email@gmail.com"
    gmail_password = "your_app_password"
    
    # Initialize the crew
    crew = StudentSelectionCrew(
        credentials_file=credentials_file,
        sheet_id=sheet_id,
        gmail_username=gmail_username,
        gmail_password=gmail_password
    )
    
    # Example quiz questions
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
    
    # Example student answers
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
        }
    ]
    
    # Example video data (you would have actual video files)
    video_data = [
        {
            'student_id': 'STU001',
            'video_path': '/path/to/john_doe_interview.mp4'
        },
        {
            'student_id': 'STU002',
            'video_path': '/path/to/jane_smith_interview.mp4'
        }
    ]
    
    # Google Drive link for video uploads
    drive_link = "https://drive.google.com/drive/folders/your_folder_id"
    
    print("=== STUDENT SELECTION CREW EXAMPLE ===")
    
    # Option 1: Run complete process
    print("\nRunning complete selection process...")
    results = crew.run_complete_selection_process(
        quiz_questions=quiz_questions,
        student_answers=student_answers,
        video_data=video_data,
        drive_link=drive_link
    )
    
    print(f"Process completed successfully: {results['success']}")
    
    # Option 2: Run individual steps
    print("\n=== INDIVIDUAL STEPS EXAMPLE ===")
    
    # Step 1: Create quiz questions
    print("1. Creating quiz questions...")
    success = crew.create_quiz_questions(quiz_questions)
    print(f"Quiz creation: {'Success' if success else 'Failed'}")
    
    # Step 2: Evaluate quiz submissions
    print("2. Evaluating quiz submissions...")
    evaluation_results = crew.evaluate_quiz_submissions(student_answers)
    print(f"Evaluated {len(evaluation_results)} students")
    
    # Step 3: Shortlist top students
    print("3. Shortlisting top students...")
    shortlisted = crew.shortlist_top_students(drive_link)
    print(f"Shortlisted {len(shortlisted)} students")
    
    # Step 4: Analyze video interviews
    print("4. Analyzing video interviews...")
    video_results = crew.analyze_video_interviews(video_data)
    print(f"Analyzed {len(video_results)} videos")
    
    # Step 5: Make final selection
    print("5. Making final selection...")
    final_candidates = crew.make_final_selection()
    print(f"Selected {len(final_candidates)} final candidates")
    
    # Check process status
    print("\n=== PROCESS STATUS ===")
    status = crew.get_process_status()
    for key, value in status.items():
        print(f"{key}: {value}")

def setup_example():
    """
    Example setup instructions
    """
    print("=== SETUP INSTRUCTIONS ===")
    print("""
    1. Install dependencies:
       pip install -r requirements.txt
    
    2. Set up Google Sheets API:
       - Go to Google Cloud Console
       - Create a new project or select existing
       - Enable Google Sheets API
       - Create service account credentials
       - Download credentials.json file
       - Share your Google Sheet with the service account email
    
    3. Set up Gmail API:
       - Enable 2-factor authentication on your Gmail account
       - Generate an app password
       - Use the app password in your configuration
    
    4. Set up API keys:
       - Get OpenAI API key from openai.com
       - Get Google API key from Google Cloud Console
       - Get Gemini API key from Google AI Studio
       - Get AssemblyAI API key from assemblyai.com (optional)
    
    5. Configure environment:
       - Copy .env.example to .env
       - Fill in all the required values
    
    6. Run the example:
       python example_usage.py
    """)

if __name__ == "__main__":
    # Uncomment the line below to run the example
    # main()
    
    # Show setup instructions
    setup_example()
