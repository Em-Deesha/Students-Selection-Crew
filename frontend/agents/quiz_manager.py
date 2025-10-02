"""
Agent 1: Quiz Manager
Handles admin-controlled quiz creation and management
"""
from crewai import Agent, Task
from typing import List, Dict, Any
import pandas as pd
from tools.sheets_manager import SheetsManager
from config import Config

class QuizManagerAgent:
    def __init__(self, sheets_manager: SheetsManager):
        """
        Initialize Quiz Manager Agent
        
        Args:
            sheets_manager: Google Sheets manager instance
        """
        self.sheets_manager = sheets_manager
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent"""
        return Agent(
            role="Quiz Manager",
            goal="Manage quiz questions and student data for the selection process",
            backstory="""You are an experienced educational administrator responsible for 
            creating and managing quiz questions for student selection. You ensure that 
            all quiz data is properly stored and organized for the evaluation process.""",
            verbose=True,
            allow_delegation=False,
            tools=[]  # No external tools needed for this agent
        )
    
    def create_quiz_task(self, questions_data: List[Dict[str, Any]]) -> Task:
        """
        Create a task for storing quiz questions
        
        Args:
            questions_data: List of question dictionaries with keys:
                - question: The question text
                - options: List of answer options
                - correct_answer: Index of correct answer
                - points: Points for this question
                - category: Question category
        
        Returns:
            CrewAI Task object
        """
        return Task(
            description=f"""
            Store {len(questions_data)} quiz questions in the Google Sheet.
            Each question should include the question text, multiple choice options,
            correct answer index, points, and category.
            Ensure proper formatting and organization of the data.
            """,
            expected_output="Confirmation that all quiz questions have been stored successfully",
            agent=self.agent,
            context={"questions_data": questions_data}
        )
    
    def store_quiz_questions(self, questions_data: List[Dict[str, Any]]) -> bool:
        """
        Store quiz questions in Google Sheets
        
        Args:
            questions_data: List of question dictionaries
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Prepare data for Google Sheets
            headers = ['Question', 'Option_A', 'Option_B', 'Option_C', 'Option_D', 
                      'Correct_Answer', 'Points', 'Category']
            
            rows = [headers]
            
            for i, question in enumerate(questions_data, 1):
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
            
            # Write to Google Sheets
            self.sheets_manager.write_sheet('Quiz_Questions', rows)
            
            print(f"Successfully stored {len(questions_data)} quiz questions")
            return True
            
        except Exception as e:
            print(f"Error storing quiz questions: {e}")
            return False
    
    def get_quiz_questions(self) -> List[Dict[str, Any]]:
        """
        Retrieve quiz questions from Google Sheets
        
        Returns:
            List of question dictionaries
        """
        try:
            data = self.sheets_manager.read_sheet('Quiz_Questions')
            
            if not data:
                return []
            
            headers = data[0]
            questions = []
            
            for row in data[1:]:
                if len(row) >= len(headers):
                    question = {
                        'question': row[0],
                        'options': [row[1], row[2], row[3], row[4]],
                        'correct_answer': int(row[5]) if row[5].isdigit() else 0,
                        'points': int(row[6]) if row[6].isdigit() else 1,
                        'category': row[7]
                    }
                    questions.append(question)
            
            return questions
            
        except Exception as e:
            print(f"Error retrieving quiz questions: {e}")
            return []
    
    def create_sample_quiz(self) -> List[Dict[str, Any]]:
        """
        Create a sample quiz for testing purposes
        
        Returns:
            List of sample questions
        """
        sample_questions = [
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
        
        return sample_questions
    
    def initialize_quiz_sheet(self) -> bool:
        """
        Initialize the quiz questions sheet with headers
        
        Returns:
            True if successful
        """
        try:
            headers = [['Question', 'Option_A', 'Option_B', 'Option_C', 'Option_D', 
                       'Correct_Answer', 'Points', 'Category']]
            self.sheets_manager.write_sheet('Quiz_Questions', headers)
            print("Quiz questions sheet initialized successfully")
            return True
        except Exception as e:
            print(f"Error initializing quiz sheet: {e}")
            return False
