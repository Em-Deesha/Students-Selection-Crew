"""
Agent 5: Finalizer
Handles final top 5 selection based on video analysis
"""
from crewai import Agent, Task
from typing import List, Dict, Any
import pandas as pd
from tools.sheets_manager import SheetsManager
from tools.email_manager import EmailManager
from config import Config

class FinalizerAgent:
    def __init__(self, sheets_manager: SheetsManager, email_manager: EmailManager):
        """
        Initialize Finalizer Agent
        
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
            role="Final Selection Manager",
            goal="Select the final top 5 students based on video interview analysis",
            backstory="""You are a senior admissions officer with extensive experience in 
            final candidate selection. You make data-driven decisions based on video 
            interview performance, ensuring the best candidates are selected for the program.""",
            verbose=True,
            allow_delegation=False,
            tools=[]
        )
    
    def create_final_selection_task(self, video_analysis_results: List[Dict[str, Any]]) -> Task:
        """
        Create a task for final selection
        
        Args:
            video_analysis_results: List of video analysis results
        
        Returns:
            CrewAI Task object
        """
        return Task(
            description=f"""
            Select the final top {Config.MAX_FINAL_SELECTION} students from {len(video_analysis_results)} 
            video interview candidates. Consider:
            - Confidence and communication skills
            - AI/ML experience and technical knowledge
            - Education status (prefer graduated or final year)
            - Overall interview performance
            Send final selection emails to chosen candidates.
            """,
            expected_output="Final selection results with top 5 candidates identified and notified",
            agent=self.agent,
            context={"video_analysis_results": video_analysis_results}
        )
    
    def select_final_candidates(self, video_analysis_results: List[Dict[str, Any]], 
                               limit: int = None) -> List[Dict[str, Any]]:
        """
        Select final candidates based on video analysis
        
        Args:
            video_analysis_results: List of video analysis results
            limit: Maximum number of final candidates
        
        Returns:
            List of final selected candidates
        """
        if not video_analysis_results:
            return []
        
        # Filter successful analyses only
        successful_results = [r for r in video_analysis_results if r.get('success', False)]
        
        if not successful_results:
            return []
        
        # Apply limit
        if limit is None:
            limit = Config.MAX_FINAL_SELECTION
        
        # Calculate comprehensive score for each candidate
        for result in successful_results:
            # Base score from video analysis
            base_score = (
                result['confidence_score'] * 0.25 +
                result['ai_experience_score'] * 0.35 +
                result['communication_score'] * 0.25
            )
            
            # Education bonus
            education_bonus = 0
            if result['education_status'] == 'graduated':
                education_bonus = 1.5
            elif result['education_status'] == 'final year':
                education_bonus = 1.0
            
            # Final comprehensive score
            result['comprehensive_score'] = base_score + education_bonus
            result['education_bonus'] = education_bonus
        
        # Sort by comprehensive score (descending)
        sorted_results = sorted(successful_results, 
                              key=lambda x: x['comprehensive_score'], 
                              reverse=True)
        
        # Select top candidates
        final_candidates = sorted_results[:limit]
        
        # Add final selection metadata
        for candidate in final_candidates:
            candidate['final_selection_status'] = 'selected'
            candidate['final_selection_timestamp'] = pd.Timestamp.now().isoformat()
            candidate['final_email_sent'] = False
        
        return final_candidates
    
    def send_final_selection_notifications(self, final_candidates: List[Dict[str, Any]]) -> Dict[str, bool]:
        """
        Send final selection notification emails
        
        Args:
            final_candidates: List of final selected candidates
        
        Returns:
            Dict mapping student emails to success status
        """
        results = {}
        
        for candidate in final_candidates:
            # Extract email from candidate data
            email = candidate.get('email', '')
            
            if not email:
                print(f"No email found for candidate {candidate.get('student_id', 'Unknown')}")
                results[email] = False
                continue
            
            # Send final selection email
            success = self.email_manager.send_final_selection_notification(email)
            
            results[email] = success
            
            # Update candidate record
            candidate['final_email_sent'] = success
            candidate['final_email_timestamp'] = pd.Timestamp.now().isoformat() if success else None
        
        return results
    
    def store_final_selection_results(self, final_candidates: List[Dict[str, Any]]) -> bool:
        """
        Store final selection results in Google Sheets
        
        Args:
            final_candidates: List of final selected candidates
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Prepare data for Google Sheets
            headers = ['Student_ID', 'Email', 'Confidence_Score', 'AI_Experience_Score', 
                      'Education_Status', 'Communication_Score', 'Comprehensive_Score',
                      'Education_Bonus', 'Final_Selection_Status', 'Final_Email_Sent',
                      'Final_Email_Timestamp', 'Final_Selection_Timestamp']
            
            rows = [headers]
            
            for candidate in final_candidates:
                row = [
                    candidate['student_id'],
                    candidate.get('email', ''),
                    candidate['confidence_score'],
                    candidate['ai_experience_score'],
                    candidate['education_status'],
                    candidate['communication_score'],
                    candidate['comprehensive_score'],
                    candidate['education_bonus'],
                    candidate['final_selection_status'],
                    candidate['final_email_sent'],
                    candidate.get('final_email_timestamp', ''),
                    candidate['final_selection_timestamp']
                ]
                rows.append(row)
            
            # Write to Google Sheets
            self.sheets_manager.write_sheet('Final_Selection', rows)
            
            print(f"Successfully stored {len(final_candidates)} final selection results")
            return True
            
        except Exception as e:
            print(f"Error storing final selection results: {e}")
            return False
    
    def get_final_selection_results(self) -> List[Dict[str, Any]]:
        """
        Retrieve final selection results from Google Sheets
        
        Returns:
            List of final selection results
        """
        try:
            data = self.sheets_manager.read_sheet('Final_Selection')
            
            if not data:
                return []
            
            headers = data[0]
            results = []
            
            for row in data[1:]:
                if len(row) >= len(headers):
                    result = {
                        'student_id': row[0],
                        'email': row[1],
                        'confidence_score': float(row[2]) if row[2] else 0,
                        'ai_experience_score': float(row[3]) if row[3] else 0,
                        'education_status': row[4],
                        'communication_score': float(row[5]) if row[5] else 0,
                        'comprehensive_score': float(row[6]) if row[6] else 0,
                        'education_bonus': float(row[7]) if row[7] else 0,
                        'final_selection_status': row[8],
                        'final_email_sent': row[9].lower() == 'true' if row[9] else False,
                        'final_email_timestamp': row[10],
                        'final_selection_timestamp': row[11]
                    }
                    results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Error retrieving final selection results: {e}")
            return []
    
    def generate_selection_report(self, final_candidates: List[Dict[str, Any]]) -> str:
        """
        Generate a comprehensive selection report
        
        Args:
            final_candidates: List of final selected candidates
        
        Returns:
            Formatted selection report
        """
        if not final_candidates:
            return "No candidates selected."
        
        report = f"""
FINAL SELECTION REPORT
=====================

Total Candidates Selected: {len(final_candidates)}

SELECTED CANDIDATES:
"""
        
        for i, candidate in enumerate(final_candidates, 1):
            report += f"""
{i}. Student ID: {candidate['student_id']}
   Email: {candidate.get('email', 'N/A')}
   Confidence Score: {candidate['confidence_score']}/10
   AI Experience Score: {candidate['ai_experience_score']}/10
   Education Status: {candidate['education_status']}
   Communication Score: {candidate['communication_score']}/10
   Comprehensive Score: {candidate['comprehensive_score']:.2f}
   Education Bonus: {candidate['education_bonus']}
   Final Email Sent: {candidate['final_email_sent']}
"""
        
        # Calculate statistics
        avg_confidence = sum(c['confidence_score'] for c in final_candidates) / len(final_candidates)
        avg_ai_experience = sum(c['ai_experience_score'] for c in final_candidates) / len(final_candidates)
        avg_communication = sum(c['communication_score'] for c in final_candidates) / len(final_candidates)
        
        report += f"""

STATISTICS:
- Average Confidence Score: {avg_confidence:.2f}/10
- Average AI Experience Score: {avg_ai_experience:.2f}/10
- Average Communication Score: {avg_communication:.2f}/10

Education Distribution:
"""
        
        education_counts = {}
        for candidate in final_candidates:
            status = candidate['education_status']
            education_counts[status] = education_counts.get(status, 0) + 1
        
        for status, count in education_counts.items():
            report += f"- {status.title()}: {count} candidates\n"
        
        return report
    
    def initialize_final_selection_sheet(self) -> bool:
        """
        Initialize the final selection sheet with headers
        
        Returns:
            True if successful
        """
        try:
            headers = [['Student_ID', 'Email', 'Confidence_Score', 'AI_Experience_Score', 
                       'Education_Status', 'Communication_Score', 'Comprehensive_Score',
                       'Education_Bonus', 'Final_Selection_Status', 'Final_Email_Sent',
                       'Final_Email_Timestamp', 'Final_Selection_Timestamp']]
            self.sheets_manager.write_sheet('Final_Selection', headers)
            print("Final selection sheet initialized successfully")
            return True
        except Exception as e:
            print(f"Error initializing final selection sheet: {e}")
            return False
