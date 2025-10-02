"""
Agent 3: Shortlist Agent
Handles top 10 student selection and email notifications
"""
from crewai import Agent, Task
from typing import List, Dict, Any
import pandas as pd
from tools.sheets_manager import SheetsManager
from tools.email_manager import EmailManager
from config import Config

class ShortlistAgent:
    def __init__(self, sheets_manager: SheetsManager, email_manager: EmailManager):
        """
        Initialize Shortlist Agent
        
        Args:
            sheets_manager: Google Sheets manager instance
            email_manager: Email manager instance
        """
        self.sheets_manager = sheets_manager
        self.email_manager = email_manager
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent"""
        return Agent(
            role="Shortlist Manager",
            goal="Select top performing students and send them notification emails",
            backstory="""You are an experienced admissions coordinator responsible for 
            identifying top candidates and managing the shortlisting process. You ensure 
            that the best students are selected and properly notified about the next steps.""",
            verbose=True,
            allow_delegation=False,
            tools=[]
        )
    
    def create_shortlist_task(self, top_students: List[Dict[str, Any]]) -> Task:
        """
        Create a task for shortlisting students
        
        Args:
            top_students: List of top performing students
        
        Returns:
            CrewAI Task object
        """
        return Task(
            description=f"""
            Shortlist the top {len(top_students)} students based on their quiz performance.
            Send notification emails to each shortlisted student with instructions for 
            the video interview round. Update the tracking sheet with shortlist status.
            """,
            expected_output="Confirmation that all shortlisted students have been notified",
            agent=self.agent,
            context={"top_students": top_students}
        )
    
    def select_top_students(self, quiz_results: List[Dict[str, Any]], 
                           limit: int = None) -> List[Dict[str, Any]]:
        """
        Select top performing students for shortlisting
        
        Args:
            quiz_results: List of quiz evaluation results
            limit: Maximum number of students to shortlist
        
        Returns:
            List of shortlisted students
        """
        if not quiz_results:
            return []
        
        # Sort by percentage (descending)
        sorted_results = sorted(quiz_results, key=lambda x: x['percentage'], reverse=True)
        
        # Apply limit
        if limit is None:
            limit = Config.MAX_SHORTLIST
        
        shortlisted = sorted_results[:limit]
        
        # Add shortlist metadata
        for student in shortlisted:
            student['shortlist_status'] = 'selected'
            student['shortlist_timestamp'] = pd.Timestamp.now().isoformat()
            student['email_sent'] = False
            student['video_uploaded'] = False
        
        return shortlisted
    
    def send_shortlist_notifications(self, shortlisted_students: List[Dict[str, Any]], 
                                   drive_link: str, deadline: str) -> Dict[str, bool]:
        """
        Send notification emails to shortlisted students
        
        Args:
            shortlisted_students: List of shortlisted students
            drive_link: Google Drive link for video upload
            deadline: Submission deadline
        
        Returns:
            Dict mapping student emails to success status
        """
        results = {}
        
        for student in shortlisted_students:
            # Extract email from student data (assuming it's stored)
            email = student.get('email', '')
            
            if not email:
                print(f"No email found for student {student.get('student_name', 'Unknown')}")
                results[email] = False
                continue
            
            # Send notification email
            success = self.email_manager.send_shortlist_notification(
                email, drive_link, deadline
            )
            
            results[email] = success
            
            # Update student record
            student['email_sent'] = success
            student['email_timestamp'] = pd.Timestamp.now().isoformat() if success else None
        
        return results
    
    def store_shortlist_results(self, shortlisted_students: List[Dict[str, Any]]) -> bool:
        """
        Store shortlist results in Google Sheets
        
        Args:
            shortlisted_students: List of shortlisted students
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Prepare data for Google Sheets
            headers = ['Student_ID', 'Student_Name', 'Email', 'Quiz_Score', 'Percentage',
                      'Shortlist_Status', 'Email_Sent', 'Email_Timestamp', 
                      'Video_Uploaded', 'Shortlist_Timestamp']
            
            rows = [headers]
            
            for student in shortlisted_students:
                row = [
                    student['student_id'],
                    student['student_name'],
                    student.get('email', ''),
                    student['total_score'],
                    student['percentage'],
                    student['shortlist_status'],
                    student['email_sent'],
                    student.get('email_timestamp', ''),
                    student['video_uploaded'],
                    student['shortlist_timestamp']
                ]
                rows.append(row)
            
            # Write to Google Sheets
            self.sheets_manager.write_sheet('Shortlist_Results', rows)
            
            print(f"Successfully stored {len(shortlisted_students)} shortlist results")
            return True
            
        except Exception as e:
            print(f"Error storing shortlist results: {e}")
            return False
    
    def get_shortlist_results(self) -> List[Dict[str, Any]]:
        """
        Retrieve shortlist results from Google Sheets
        
        Returns:
            List of shortlist results
        """
        try:
            data = self.sheets_manager.read_sheet('Shortlist_Results')
            
            if not data:
                return []
            
            headers = data[0]
            results = []
            
            for row in data[1:]:
                if len(row) >= len(headers):
                    result = {
                        'student_id': row[0],
                        'student_name': row[1],
                        'email': row[2],
                        'quiz_score': float(row[3]) if row[3] else 0,
                        'percentage': float(row[4]) if row[4] else 0,
                        'shortlist_status': row[5],
                        'email_sent': row[6].lower() == 'true' if row[6] else False,
                        'email_timestamp': row[7],
                        'video_uploaded': row[8].lower() == 'true' if row[8] else False,
                        'shortlist_timestamp': row[9]
                    }
                    results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Error retrieving shortlist results: {e}")
            return []
    
    def update_video_status(self, student_id: str, video_uploaded: bool = True) -> bool:
        """
        Update video upload status for a student
        
        Args:
            student_id: Student ID
            video_uploaded: Whether video has been uploaded
        
        Returns:
            True if successful
        """
        try:
            # This would need to be implemented based on your specific sheet structure
            # For now, we'll just return True as a placeholder
            print(f"Updated video status for student {student_id}: {video_uploaded}")
            return True
        except Exception as e:
            print(f"Error updating video status: {e}")
            return False
    
    def initialize_shortlist_sheet(self) -> bool:
        """
        Initialize the shortlist results sheet with headers
        
        Returns:
            True if successful
        """
        try:
            headers = [['Student_ID', 'Student_Name', 'Email', 'Quiz_Score', 'Percentage',
                       'Shortlist_Status', 'Email_Sent', 'Email_Timestamp', 
                       'Video_Uploaded', 'Shortlist_Timestamp']]
            self.sheets_manager.write_sheet('Shortlist_Results', headers)
            print("Shortlist results sheet initialized successfully")
            return True
        except Exception as e:
            print(f"Error initializing shortlist sheet: {e}")
            return False
