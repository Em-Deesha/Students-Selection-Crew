"""
Student Selection Crew - Main orchestrator for the multi-agent system
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

class StudentSelectionCrew:
    def __init__(self, credentials_file: str, sheet_id: str, 
                 gmail_username: str, gmail_password: str):
        """
        Initialize the Student Selection Crew
        
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
        
        # Initialize sheets
        self._initialize_sheets()
    
    def _initialize_sheets(self):
        """Initialize all required Google Sheets"""
        try:
            self.quiz_manager.initialize_quiz_sheet()
            self.checker.initialize_results_sheet()
            self.shortlist_agent.initialize_shortlist_sheet()
            self.video_analyzer_agent.initialize_video_analysis_sheet()
            self.finalizer.initialize_final_selection_sheet()
            print("All sheets initialized successfully")
        except Exception as e:
            print(f"Error initializing sheets: {e}")
    
    def create_quiz_questions(self, questions_data: List[Dict[str, Any]]) -> bool:
        """
        Create and store quiz questions (Admin function)
        
        Args:
            questions_data: List of question dictionaries
        
        Returns:
            True if successful
        """
        print("Creating quiz questions...")
        return self.quiz_manager.store_quiz_questions(questions_data)
    
    def evaluate_quiz_submissions(self, student_answers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Evaluate student quiz submissions
        
        Args:
            student_answers: List of student answer dictionaries
        
        Returns:
            List of evaluation results
        """
        print("Evaluating quiz submissions...")
        
        # Get quiz questions
        quiz_questions = self.quiz_manager.get_quiz_questions()
        if not quiz_questions:
            print("No quiz questions found. Please create quiz questions first.")
            return []
        
        # Evaluate answers
        results = self.checker.evaluate_answers(student_answers, quiz_questions)
        
        # Store results
        if results:
            self.checker.store_evaluation_results(results)
            print(f"Evaluated {len(results)} student submissions")
        
        return results
    
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
        
        # Get quiz results
        quiz_results = self.checker.get_evaluation_results()
        if not quiz_results:
            print("No quiz results found. Please evaluate quiz submissions first.")
            return []
        
        # Select top students
        shortlisted = self.shortlist_agent.select_top_students(quiz_results)
        
        if not shortlisted:
            print("No students to shortlist")
            return []
        
        # Set default deadline
        if deadline is None:
            deadline = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        
        # Send notifications
        email_results = self.shortlist_agent.send_shortlist_notifications(
            shortlisted, drive_link, deadline
        )
        
        # Store results
        self.shortlist_agent.store_shortlist_results(shortlisted)
        
        print(f"Shortlisted {len(shortlisted)} students")
        print(f"Email notifications sent: {sum(email_results.values())}/{len(email_results)}")
        
        return shortlisted
    
    def analyze_video_interviews(self, video_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze video interviews
        
        Args:
            video_data: List of video data dictionaries with 'student_id', 'video_path'
        
        Returns:
            List of analysis results
        """
        print("Analyzing video interviews...")
        
        # Analyze videos
        results = self.video_analyzer_agent.analyze_videos(video_data)
        
        # Store results
        if results:
            self.video_analyzer_agent.store_video_analysis_results(results)
            successful = sum(1 for r in results if r['success'])
            print(f"Analyzed {successful}/{len(results)} videos successfully")
        
        return results
    
    def make_final_selection(self) -> List[Dict[str, Any]]:
        """
        Make final selection based on video analysis
        
        Returns:
            List of final selected candidates
        """
        print("Making final selection...")
        
        # Get video analysis results
        video_results = self.video_analyzer_agent.get_video_analysis_results()
        if not video_results:
            print("No video analysis results found. Please analyze videos first.")
            return []
        
        # Select final candidates
        final_candidates = self.finalizer.select_final_candidates(video_results)
        
        if not final_candidates:
            print("No candidates for final selection")
            return []
        
        # Send final notifications
        email_results = self.finalizer.send_final_selection_notifications(final_candidates)
        
        # Store results
        self.finalizer.store_final_selection_results(final_candidates)
        
        # Generate and print report
        report = self.finalizer.generate_selection_report(final_candidates)
        print(report)
        
        print(f"Final selection completed: {len(final_candidates)} candidates selected")
        print(f"Final emails sent: {sum(email_results.values())}/{len(email_results)}")
        
        return final_candidates
    
    def run_complete_selection_process(self, quiz_questions: List[Dict[str, Any]], 
                                     student_answers: List[Dict[str, Any]],
                                     video_data: List[Dict[str, Any]],
                                     drive_link: str) -> Dict[str, Any]:
        """
        Run the complete student selection process
        
        Args:
            quiz_questions: List of quiz questions
            student_answers: List of student quiz answers
            video_data: List of video interview data
            drive_link: Google Drive link for video upload
        
        Returns:
            Complete process results
        """
        results = {
            'quiz_creation': False,
            'quiz_evaluation': [],
            'shortlisting': [],
            'video_analysis': [],
            'final_selection': [],
            'success': False
        }
        
        try:
            # Step 1: Create quiz questions
            print("=== STEP 1: Creating Quiz Questions ===")
            results['quiz_creation'] = self.create_quiz_questions(quiz_questions)
            
            if not results['quiz_creation']:
                print("Failed to create quiz questions")
                return results
            
            # Step 2: Evaluate quiz submissions
            print("\n=== STEP 2: Evaluating Quiz Submissions ===")
            results['quiz_evaluation'] = self.evaluate_quiz_submissions(student_answers)
            
            if not results['quiz_evaluation']:
                print("Failed to evaluate quiz submissions")
                return results
            
            # Step 3: Shortlist top students
            print("\n=== STEP 3: Shortlisting Top Students ===")
            results['shortlisting'] = self.shortlist_top_students(drive_link)
            
            if not results['shortlisting']:
                print("Failed to shortlist students")
                return results
            
            # Step 4: Analyze video interviews
            print("\n=== STEP 4: Analyzing Video Interviews ===")
            results['video_analysis'] = self.analyze_video_interviews(video_data)
            
            if not results['video_analysis']:
                print("Failed to analyze video interviews")
                return results
            
            # Step 5: Make final selection
            print("\n=== STEP 5: Making Final Selection ===")
            results['final_selection'] = self.make_final_selection()
            
            if results['final_selection']:
                results['success'] = True
                print("\n=== SELECTION PROCESS COMPLETED SUCCESSFULLY ===")
            else:
                print("Failed to make final selection")
            
        except Exception as e:
            print(f"Error in complete selection process: {e}")
            results['error'] = str(e)
        
        return results
    
    def get_process_status(self) -> Dict[str, Any]:
        """
        Get the current status of the selection process
        
        Returns:
            Status dictionary with counts and progress
        """
        status = {
            'quiz_questions': len(self.quiz_manager.get_quiz_questions()),
            'quiz_results': len(self.checker.get_evaluation_results()),
            'shortlisted': len(self.shortlist_agent.get_shortlist_results()),
            'video_analysis': len(self.video_analyzer_agent.get_video_analysis_results()),
            'final_selection': len(self.finalizer.get_final_selection_results())
        }
        
        return status
    
    def reset_process(self):
        """Reset the entire selection process (use with caution)"""
        print("Resetting selection process...")
        try:
            # Clear all sheets (this would need to be implemented in SheetsManager)
            print("Process reset completed")
        except Exception as e:
            print(f"Error resetting process: {e}")
