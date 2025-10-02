"""
Fixed Student Selection Crew - Works with your existing Google Sheet structure
"""
from crewai import Crew, Process
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime, timedelta

# Import agents
from agents.quiz_manager import QuizManagerAgent
from agents.checker import CheckerAgent
from agents.shortlist_agent import ShortlistAgent
from agents.video_analyzer_agent import VideoAnalyzerAgent
from agents.finalizer import FinalizerAgent

# Import tools
from tools.sheets_manager import SheetsManager
from tools.email_manager import EmailManager
from tools.video_analyzer import VideoAnalyzer

# Import configuration
from config import Config

class FixedStudentSelectionCrew:
    def __init__(self, credentials_file: str, sheet_id: str, 
                 gmail_username: str, gmail_password: str):
        """
        Initialize the Fixed Student Selection Crew
        
        Args:
            credentials_file: Path to Google service account credentials
            sheet_id: Google Sheets document ID
            gmail_username: Gmail username for sending emails
            gmail_password: Gmail app password
        """
        # Initialize tools
        self.sheets_manager = SheetsManager(credentials_file, sheet_id)
        self.email_manager = EmailManager(gmail_username, gmail_password)
        self.video_analyzer = VideoAnalyzer()
        
        # Initialize agents
        self.quiz_manager = QuizManagerAgent(self.sheets_manager)
        self.checker = CheckerAgent(self.sheets_manager)
        self.shortlist_agent = ShortlistAgent(self.sheets_manager, self.email_manager)
        self.video_analyzer_agent = VideoAnalyzerAgent(self.sheets_manager, self.video_analyzer)
        self.finalizer = FinalizerAgent(self.sheets_manager, self.email_manager)
        
        # Initialize your existing sheet structure
        self._initialize_your_sheet()
    
    def _initialize_your_sheet(self):
        """Initialize your existing Google Sheet with proper structure"""
        try:
            # Your sheet already has the right structure, just ensure headers are correct
            headers = [
                'Student Name', 'Email', 'Quiz Marks', 'Status', 
                'Video Link', 'Transcript', 'Confidence', 'AI Experience', 'Final Result'
            ]
            
            # Check if headers exist
            try:
                existing_data = self.sheets_manager.read_sheet('Sheet1', 'A1:I1')
                if not existing_data or existing_data[0] != headers:
                    # Update headers if needed
                    self.sheets_manager.write_sheet('Sheet1', [headers], 'A1')
                    print("✅ Updated sheet headers")
                else:
                    print("✅ Sheet headers already correct")
            except Exception as e:
                print(f"⚠️ Could not check headers: {e}")
                
        except Exception as e:
            print(f"Error initializing sheet: {e}")
    
    def create_quiz_questions(self, questions_data: List[Dict[str, Any]]) -> bool:
        """
        Create and store quiz questions (Admin function)
        
        Args:
            questions_data: List of question dictionaries
        
        Returns:
            True if successful
        """
        print("Creating quiz questions...")
        try:
            # Store quiz questions in a separate area of your sheet
            # We'll use columns J onwards for quiz data
            quiz_headers = ['Question', 'Option_A', 'Option_B', 'Option_C', 'Option_D', 
                           'Correct_Answer', 'Points', 'Category']
            
            rows = [quiz_headers]
            
            for question in questions_data:
                row = [
                    question['question'],
                    question['options'][0] if len(question['options']) > 0 else '',
                    question['options'][1] if len(question['options']) > 1 else '',
                    question['options'][2] if len(question['options']) > 2 else '',
                    question['options'][3] if len(question['options']) > 3 else '',
                    question['correct_answer'],
                    question['points'],
                    question['category']
                ]
                rows.append(row)
            
            # Write to columns J onwards
            self.sheets_manager.write_sheet('Sheet1', rows, 'J1')
            print(f"✅ Successfully stored {len(questions_data)} quiz questions")
            return True
            
        except Exception as e:
            print(f"❌ Error storing quiz questions: {e}")
            return False
    
    def evaluate_quiz_submissions(self, student_answers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Evaluate student quiz submissions
        
        Args:
            student_answers: List of student answer dictionaries
        
        Returns:
            List of evaluation results
        """
        print("Evaluating quiz submissions...")
        
        try:
            # Get quiz questions from columns J onwards
            quiz_data = self.sheets_manager.read_sheet('Sheet1', 'J:Z')
            
            if not quiz_data or len(quiz_data) < 2:
                print("❌ No quiz questions found. Please create quiz questions first.")
                return []
            
            # Parse quiz questions
            quiz_questions = []
            for row in quiz_data[1:]:  # Skip header
                if len(row) >= 8:
                    question = {
                        'question': row[0],
                        'options': [row[1], row[2], row[3], row[4]],
                        'correct_answer': int(row[5]) if str(row[5]).isdigit() else 0,
                        'points': int(row[6]) if str(row[6]).isdigit() else 1,
                        'category': row[7]
                    }
                    quiz_questions.append(question)
            
            # Evaluate answers
            results = self.checker.evaluate_answers(student_answers, quiz_questions)
            
            # Store results in your main sheet
            if results:
                # Update the main sheet with student data
                for i, result in enumerate(results, 2):  # Start from row 2 (after headers)
                    student_data = [
                        result['student_name'],
                        result.get('email', ''),
                        result['total_score'],
                        'Quiz Completed',
                        '',  # Video Link
                        '',  # Transcript
                        '',  # Confidence
                        '',  # AI Experience
                        ''   # Final Result
                    ]
                    
                    # Write to the main sheet
                    self.sheets_manager.write_sheet('Sheet1', [student_data], f'A{i}')
                
                print(f"✅ Evaluated {len(results)} student submissions")
            
            return results
            
        except Exception as e:
            print(f"❌ Error evaluating submissions: {e}")
            return []
    
    def shortlist_top_students(self, drive_link: str, deadline: str = None) -> List[Dict[str, Any]]:
        """
        Shortlist top students and send notifications
        
        Args:
            drive_link: Google Drive link for video upload
            deadline: Submission deadline (default: 7 days from now)
        
        Returns:
            List of shortlisted students
        """
        print("Shortlisting top students...")
        
        try:
            # Get student data from your sheet
            student_data = self.sheets_manager.read_sheet('Sheet1', 'A:I')
            
            if not student_data or len(student_data) < 2:
                print("❌ No student data found. Please evaluate quiz submissions first.")
                return []
            
            # Parse student results
            students = []
            for row in student_data[1:]:  # Skip header
                if len(row) >= 3 and row[2]:  # Has quiz marks
                    student = {
                        'student_id': f"STU{len(students)+1:03d}",
                        'student_name': row[0],
                        'email': row[1],
                        'total_score': float(row[2]) if str(row[2]).replace('.', '').isdigit() else 0,
                        'percentage': float(row[2]) if str(row[2]).replace('.', '').isdigit() else 0
                    }
                    students.append(student)
            
            if not students:
                print("❌ No students with quiz results found")
                return []
            
            # Sort by score and select top students
            students.sort(key=lambda x: x['total_score'], reverse=True)
            shortlisted = students[:Config.MAX_SHORTLIST]
            
            # Update status in sheet
            for i, student in enumerate(shortlisted, 2):
                # Update status to "Shortlisted"
                self.sheets_manager.update_cell('Sheet1', f'D{i}', 'Shortlisted')
            
            # Send notifications
            if deadline is None:
                deadline = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            
            email_results = self.shortlist_agent.send_shortlist_notifications(
                shortlisted, drive_link, deadline
            )
            
            print(f"✅ Shortlisted {len(shortlisted)} students")
            print(f"📧 Email notifications sent: {sum(email_results.values())}/{len(email_results)}")
            
            return shortlisted
            
        except Exception as e:
            print(f"❌ Error shortlisting students: {e}")
            return []
    
    def analyze_video_interviews(self, video_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze video interviews
        
        Args:
            video_data: List of video data dictionaries with 'student_id', 'video_path'
        
        Returns:
            List of analysis results
        """
        print("Analyzing video interviews...")
        
        try:
            # Analyze videos
            results = self.video_analyzer_agent.analyze_videos(video_data)
            
            # Update your sheet with video analysis results
            if results:
                for result in results:
                    # Find the student in your sheet and update their data
                    student_data = self.sheets_manager.read_sheet('Sheet1', 'A:I')
                    
                    for i, row in enumerate(student_data[1:], 2):  # Skip header, start from row 2
                        if len(row) >= 1 and row[0]:  # Has student name
                            # Update video analysis data
                            if result['success']:
                                self.sheets_manager.update_cell('Sheet1', f'E{i}', 'Video Uploaded')
                                self.sheets_manager.update_cell('Sheet1', f'F{i}', result['transcript'][:100] + '...')
                                self.sheets_manager.update_cell('Sheet1', f'G{i}', str(result['confidence_score']))
                                self.sheets_manager.update_cell('Sheet1', f'H{i}', str(result['ai_experience_score']))
                            
                successful = sum(1 for r in results if r['success'])
                print(f"✅ Analyzed {successful}/{len(results)} videos successfully")
            
            return results
            
        except Exception as e:
            print(f"❌ Error analyzing videos: {e}")
            return []
    
    def make_final_selection(self) -> List[Dict[str, Any]]:
        """
        Make final selection based on video analysis
        
        Returns:
            List of final selected candidates
        """
        print("Making final selection...")
        
        try:
            # Get student data from your sheet
            student_data = self.sheets_manager.read_sheet('Sheet1', 'A:I')
            
            if not student_data or len(student_data) < 2:
                print("❌ No student data found.")
                return []
            
            # Parse students with video analysis
            candidates = []
            for row in student_data[1:]:  # Skip header
                if len(row) >= 8 and row[6] and row[7]:  # Has confidence and AI experience scores
                    candidate = {
                        'student_id': f"STU{len(candidates)+1:03d}",
                        'student_name': row[0],
                        'email': row[1],
                        'confidence_score': float(row[6]) if str(row[6]).replace('.', '').isdigit() else 0,
                        'ai_experience_score': float(row[7]) if str(row[7]).replace('.', '').isdigit() else 0,
                        'education_status': 'graduated'  # Default
                    }
                    candidates.append(candidate)
            
            if not candidates:
                print("❌ No candidates with video analysis found")
                return []
            
            # Select final candidates
            final_candidates = self.finalizer.select_final_candidates(candidates)
            
            # Update final results in sheet
            for i, candidate in enumerate(final_candidates, 2):
                # Find the candidate in the sheet and update final result
                for j, row in enumerate(student_data[1:], 2):
                    if len(row) >= 1 and row[0] == candidate['student_name']:
                        self.sheets_manager.update_cell('Sheet1', f'I{j}', 'Selected')
                        break
            
            # Send final notifications
            email_results = self.finalizer.send_final_selection_notifications(final_candidates)
            
            print(f"✅ Final selection completed: {len(final_candidates)} candidates selected")
            print(f"📧 Final emails sent: {sum(email_results.values())}/{len(email_results)}")
            
            return final_candidates
            
        except Exception as e:
            print(f"❌ Error making final selection: {e}")
            return []
    
    def get_process_status(self) -> Dict[str, Any]:
        """
        Get the current status of the selection process
        
        Returns:
            Status dictionary with counts and progress
        """
        try:
            # Get data from your sheet
            student_data = self.sheets_manager.read_sheet('Sheet1', 'A:I')
            
            if not student_data or len(student_data) < 2:
                return {
                    'quiz_questions': 0,
                    'quiz_results': 0,
                    'shortlisted': 0,
                    'video_analysis': 0,
                    'final_selection': 0
                }
            
            # Count different statuses
            quiz_results = 0
            shortlisted = 0
            video_analysis = 0
            final_selection = 0
            
            for row in student_data[1:]:  # Skip header
                if len(row) >= 4:
                    if row[2] and str(row[2]).replace('.', '').isdigit():  # Has quiz marks
                        quiz_results += 1
                    if row[3] == 'Shortlisted':  # Shortlisted
                        shortlisted += 1
                    if row[6] and str(row[6]).replace('.', '').isdigit():  # Has confidence score
                        video_analysis += 1
                    if row[8] == 'Selected':  # Final selection
                        final_selection += 1
            
            return {
                'quiz_questions': 1,  # We have quiz questions stored
                'quiz_results': quiz_results,
                'shortlisted': shortlisted,
                'video_analysis': video_analysis,
                'final_selection': final_selection
            }
            
        except Exception as e:
            print(f"Error getting status: {e}")
            return {
                'quiz_questions': 0,
                'quiz_results': 0,
                'shortlisted': 0,
                'video_analysis': 0,
                'final_selection': 0
            }
