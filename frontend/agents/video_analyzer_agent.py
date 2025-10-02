"""
Agent 4: Video Analyzer Agent
Handles video analysis and transcript processing
"""
from crewai import Agent, Task
from typing import List, Dict, Any
import pandas as pd
from tools.sheets_manager import SheetsManager
from tools.video_analyzer import VideoAnalyzer
from config import Config

class VideoAnalyzerAgent:
    def __init__(self, sheets_manager: SheetsManager, video_analyzer: VideoAnalyzer):
        """
        Initialize Video Analyzer Agent
        
        Args:
            sheets_manager: Google Sheets manager instance
            video_analyzer: Video analyzer tool instance
        """
        self.sheets_manager = sheets_manager
        self.video_analyzer = video_analyzer
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent"""
        return Agent(
            role="Video Interview Analyzer",
            goal="Analyze student video interviews for confidence, AI experience, and education status",
            backstory="""You are an expert in video interview analysis with deep understanding of 
            student assessment criteria. You evaluate communication skills, technical knowledge, 
            and educational background to provide comprehensive candidate insights.""",
            verbose=True,
            allow_delegation=False,
            tools=[]
        )
    
    def create_video_analysis_task(self, video_paths: List[str]) -> Task:
        """
        Create a task for analyzing video interviews
        
        Args:
            video_paths: List of video file paths to analyze
        
        Returns:
            CrewAI Task object
        """
        return Task(
            description=f"""
            Analyze {len(video_paths)} student video interviews.
            For each video, extract the transcript and analyze:
            - Confidence level and communication skills
            - AI/ML experience and technical knowledge
            - Education status and background
            - Overall interview performance
            Store all results with detailed analysis.
            """,
            expected_output="Complete analysis results for all video interviews",
            agent=self.agent,
            context={"video_paths": video_paths}
        )
    
    def analyze_videos(self, video_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze multiple video interviews
        
        Args:
            video_data: List of video data dictionaries with 'student_id', 'video_path'
        
        Returns:
            List of analysis results
        """
        results = []
        
        for video_info in video_data:
            student_id = video_info.get('student_id', 'Unknown')
            video_path = video_info.get('video_path', '')
            
            print(f"Analyzing video for student {student_id}...")
            
            # Analyze the video
            analysis_result = self.video_analyzer.analyze_video_complete(video_path)
            
            if analysis_result['success']:
                # Combine with student info
                result = {
                    'student_id': student_id,
                    'video_path': video_path,
                    'transcript': analysis_result['transcript'],
                    'confidence_score': analysis_result['analysis']['confidence_score'],
                    'ai_experience_score': analysis_result['analysis']['ai_experience_score'],
                    'education_status': analysis_result['analysis']['education_status'],
                    'communication_score': analysis_result['analysis']['communication_score'],
                    'detailed_analysis': analysis_result['analysis']['detailed_analysis'],
                    'analysis_timestamp': pd.Timestamp.now().isoformat(),
                    'success': True
                }
            else:
                result = {
                    'student_id': student_id,
                    'video_path': video_path,
                    'transcript': '',
                    'confidence_score': 0,
                    'ai_experience_score': 0,
                    'education_status': 'unknown',
                    'communication_score': 0,
                    'detailed_analysis': f"Analysis failed: {analysis_result.get('error', 'Unknown error')}",
                    'analysis_timestamp': pd.Timestamp.now().isoformat(),
                    'success': False
                }
            
            results.append(result)
        
        return results
    
    def store_video_analysis_results(self, results: List[Dict[str, Any]]) -> bool:
        """
        Store video analysis results in Google Sheets
        
        Args:
            results: List of analysis results
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Prepare data for Google Sheets
            headers = ['Student_ID', 'Video_Path', 'Transcript', 'Confidence_Score', 
                      'AI_Experience_Score', 'Education_Status', 'Communication_Score',
                      'Detailed_Analysis', 'Analysis_Timestamp', 'Success']
            
            rows = [headers]
            
            for result in results:
                row = [
                    result['student_id'],
                    result['video_path'],
                    result['transcript'][:1000] + '...' if len(result['transcript']) > 1000 else result['transcript'],
                    result['confidence_score'],
                    result['ai_experience_score'],
                    result['education_status'],
                    result['communication_score'],
                    result['detailed_analysis'][:500] + '...' if len(result['detailed_analysis']) > 500 else result['detailed_analysis'],
                    result['analysis_timestamp'],
                    result['success']
                ]
                rows.append(row)
            
            # Write to Google Sheets
            self.sheets_manager.write_sheet('Video_Analysis', rows)
            
            print(f"Successfully stored {len(results)} video analysis results")
            return True
            
        except Exception as e:
            print(f"Error storing video analysis results: {e}")
            return False
    
    def get_video_analysis_results(self) -> List[Dict[str, Any]]:
        """
        Retrieve video analysis results from Google Sheets
        
        Returns:
            List of analysis results
        """
        try:
            data = self.sheets_manager.read_sheet('Video_Analysis')
            
            if not data:
                return []
            
            headers = data[0]
            results = []
            
            for row in data[1:]:
                if len(row) >= len(headers):
                    result = {
                        'student_id': row[0],
                        'video_path': row[1],
                        'transcript': row[2],
                        'confidence_score': float(row[3]) if row[3] else 0,
                        'ai_experience_score': float(row[4]) if row[4] else 0,
                        'education_status': row[5],
                        'communication_score': float(row[6]) if row[6] else 0,
                        'detailed_analysis': row[7],
                        'analysis_timestamp': row[8],
                        'success': row[9].lower() == 'true' if row[9] else False
                    }
                    results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Error retrieving video analysis results: {e}")
            return []
    
    def get_top_video_candidates(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get top candidates based on video analysis
        
        Args:
            limit: Number of top candidates to return
        
        Returns:
            List of top candidates sorted by combined score
        """
        results = self.get_video_analysis_results()
        
        if not results:
            return []
        
        # Filter successful analyses only
        successful_results = [r for r in results if r['success']]
        
        if not successful_results:
            return []
        
        # Calculate combined score (weighted average)
        for result in successful_results:
            combined_score = (
                result['confidence_score'] * 0.3 +
                result['ai_experience_score'] * 0.4 +
                result['communication_score'] * 0.3
            )
            result['combined_score'] = combined_score
        
        # Sort by combined score (descending)
        sorted_results = sorted(successful_results, key=lambda x: x['combined_score'], reverse=True)
        
        return sorted_results[:limit]
    
    def initialize_video_analysis_sheet(self) -> bool:
        """
        Initialize the video analysis sheet with headers
        
        Returns:
            True if successful
        """
        try:
            headers = [['Student_ID', 'Video_Path', 'Transcript', 'Confidence_Score', 
                       'AI_Experience_Score', 'Education_Status', 'Communication_Score',
                       'Detailed_Analysis', 'Analysis_Timestamp', 'Success']]
            self.sheets_manager.write_sheet('Video_Analysis', headers)
            print("Video analysis sheet initialized successfully")
            return True
        except Exception as e:
            print(f"Error initializing video analysis sheet: {e}")
            return False
