"""
Agent 2: Checker
Handles automated answer evaluation and scoring
"""
from crewai import Agent, Task
from typing import List, Dict, Any
import pandas as pd
from tools.sheets_manager import SheetsManager
from config import Config

class CheckerAgent:
    def __init__(self, sheets_manager: SheetsManager):
        """
        Initialize Checker Agent
        
        Args:
            sheets_manager: Google Sheets manager instance
        """
        self.sheets_manager = sheets_manager
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent"""
        return Agent(
            role="Answer Checker",
            goal="Evaluate student quiz answers and calculate scores accurately",
            backstory="""You are an experienced educational evaluator with expertise in 
            automated assessment systems. You ensure fair and accurate evaluation of 
            student responses using provided answer keys.""",
            verbose=True,
            allow_delegation=False,
            tools=[]
        )
    
    def create_evaluation_task(self, student_answers: List[Dict[str, Any]]) -> Task:
        """
        Create a task for evaluating student answers
        
        Args:
            student_answers: List of student answer dictionaries
        
        Returns:
            CrewAI Task object
        """
        return Task(
            description=f"""
            Evaluate {len(student_answers)} student quiz submissions.
            Compare each answer against the correct answer key and calculate scores.
            Store the results with student information and scores.
            """,
            expected_output="Complete evaluation results with scores for all students",
            agent=self.agent,
            context={"student_answers": student_answers}
        )
    
    def evaluate_answers(self, student_answers: List[Dict[str, Any]], 
                        quiz_questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Evaluate student answers against the answer key
        
        Args:
            student_answers: List of student answer dictionaries
            quiz_questions: List of quiz questions with correct answers
        
        Returns:
            List of evaluation results
        """
        results = []
        
        for student in student_answers:
            student_id = student.get('student_id', 'Unknown')
            student_name = student.get('name', 'Unknown')
            answers = student.get('answers', [])
            
            total_score = 0
            max_possible = 0
            correct_answers = 0
            
            evaluation_details = []
            
            for i, answer in enumerate(answers):
                if i < len(quiz_questions):
                    question = quiz_questions[i]
                    correct_answer = question['correct_answer']
                    points = question['points']
                    
                    max_possible += points
                    
                    is_correct = (answer == correct_answer)
                    if is_correct:
                        total_score += points
                        correct_answers += 1
                    
                    evaluation_details.append({
                        'question_index': i,
                        'student_answer': answer,
                        'correct_answer': correct_answer,
                        'is_correct': is_correct,
                        'points_earned': points if is_correct else 0,
                        'max_points': points
                    })
            
            percentage = (total_score / max_possible * 100) if max_possible > 0 else 0
            
            result = {
                'student_id': student_id,
                'student_name': student_name,
                'total_score': total_score,
                'max_possible': max_possible,
                'percentage': round(percentage, 2),
                'correct_answers': correct_answers,
                'total_questions': len(quiz_questions),
                'evaluation_details': evaluation_details,
                'timestamp': pd.Timestamp.now().isoformat()
            }
            
            results.append(result)
        
        return results
    
    def store_evaluation_results(self, results: List[Dict[str, Any]]) -> bool:
        """
        Store evaluation results in Google Sheets
        
        Args:
            results: List of evaluation results
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Prepare data for Google Sheets
            headers = ['Student_ID', 'Student_Name', 'Total_Score', 'Max_Possible', 
                      'Percentage', 'Correct_Answers', 'Total_Questions', 'Timestamp']
            
            rows = [headers]
            
            for result in results:
                row = [
                    result['student_id'],
                    result['student_name'],
                    result['total_score'],
                    result['max_possible'],
                    result['percentage'],
                    result['correct_answers'],
                    result['total_questions'],
                    result['timestamp']
                ]
                rows.append(row)
            
            # Write to Google Sheets
            self.sheets_manager.write_sheet('Quiz_Results', rows)
            
            print(f"Successfully stored {len(results)} evaluation results")
            return True
            
        except Exception as e:
            print(f"Error storing evaluation results: {e}")
            return False
    
    def get_evaluation_results(self) -> List[Dict[str, Any]]:
        """
        Retrieve evaluation results from Google Sheets
        
        Returns:
            List of evaluation results
        """
        try:
            data = self.sheets_manager.read_sheet('Quiz_Results')
            
            if not data:
                return []
            
            headers = data[0]
            results = []
            
            for row in data[1:]:
                if len(row) >= len(headers):
                    result = {
                        'student_id': row[0],
                        'student_name': row[1],
                        'total_score': float(row[2]) if row[2] else 0,
                        'max_possible': float(row[3]) if row[3] else 0,
                        'percentage': float(row[4]) if row[4] else 0,
                        'correct_answers': int(row[5]) if row[5] else 0,
                        'total_questions': int(row[6]) if row[6] else 0,
                        'timestamp': row[7]
                    }
                    results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Error retrieving evaluation results: {e}")
            return []
    
    def get_top_students(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top performing students based on quiz scores
        
        Args:
            limit: Number of top students to return
        
        Returns:
            List of top students sorted by percentage
        """
        results = self.get_evaluation_results()
        
        if not results:
            return []
        
        # Sort by percentage (descending)
        sorted_results = sorted(results, key=lambda x: x['percentage'], reverse=True)
        
        return sorted_results[:limit]
    
    def initialize_results_sheet(self) -> bool:
        """
        Initialize the quiz results sheet with headers
        
        Returns:
            True if successful
        """
        try:
            headers = [['Student_ID', 'Student_Name', 'Total_Score', 'Max_Possible', 
                       'Percentage', 'Correct_Answers', 'Total_Questions', 'Timestamp']]
            self.sheets_manager.write_sheet('Quiz_Results', headers)
            print("Quiz results sheet initialized successfully")
            return True
        except Exception as e:
            print(f"Error initializing results sheet: {e}")
            return False
