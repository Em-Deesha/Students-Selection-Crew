"""
Video analysis tools for speech-to-text and content analysis
"""
import os
import tempfile
from typing import Dict, Any, List
import whisper
import google.generativeai as genai
from config import Config

class VideoAnalyzer:
    def __init__(self, gemini_api_key: str = None):
        """
        Initialize Video Analyzer
        
        Args:
            gemini_api_key: Google Gemini API key
        """
        self.gemini_api_key = gemini_api_key or Config.GEMINI_API_KEY
        
        # Initialize Whisper model
        self.whisper_model = whisper.load_model("base")
        
        # Initialize Gemini
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
        else:
            self.gemini_model = None
    
    def extract_audio_from_video(self, video_path: str) -> str:
        """
        Extract audio from video file
        
        Args:
            video_path: Path to video file
        
        Returns:
            Path to extracted audio file
        """
        try:
            import subprocess
            
            # Create temporary audio file
            audio_path = tempfile.mktemp(suffix='.wav')
            
            # Use ffmpeg to extract audio
            cmd = [
                'ffmpeg', '-i', video_path, 
                '-vn', '-acodec', 'pcm_s16le', 
                '-ar', '16000', '-ac', '1', 
                audio_path, '-y'
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            return audio_path
            
        except Exception as e:
            print(f"Error extracting audio: {e}")
            return None
    
    def transcribe_video(self, video_path: str) -> str:
        """
        Transcribe video to text using Whisper
        
        Args:
            video_path: Path to video file
        
        Returns:
            Transcribed text
        """
        try:
            # Extract audio first
            audio_path = self.extract_audio_from_video(video_path)
            
            if not audio_path:
                return None
            
            # Transcribe using Whisper
            result = self.whisper_model.transcribe(audio_path)
            transcript = result["text"]
            
            # Clean up temporary audio file
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            return transcript.strip()
            
        except Exception as e:
            print(f"Error transcribing video: {e}")
            return None
    
    def analyze_transcript(self, transcript: str) -> Dict[str, Any]:
        """
        Analyze transcript for confidence, AI experience, and education status
        
        Args:
            transcript: Transcribed text
        
        Returns:
            Analysis results
        """
        if not self.gemini_model:
            return self._fallback_analysis(transcript)
        
        try:
            prompt = f"""
            Analyze the following interview transcript for a student selection process.
            Provide scores (1-10) and detailed analysis for:
            
            1. Confidence (tone, fluency, clarity)
            2. AI/ML Experience (mentions of AI, ML, data science, programming)
            3. Education Status (graduated, final year, etc.)
            4. Overall Communication Skills
            
            Transcript: {transcript}
            
            Please provide your analysis in the following format:
            Confidence Score: X/10
            AI Experience Score: X/10
            Education Status: [graduated/final year/other]
            Communication Score: X/10
            
            Detailed Analysis:
            - Confidence: [detailed analysis]
            - AI Experience: [detailed analysis]
            - Education: [detailed analysis]
            - Communication: [detailed analysis]
            """
            
            response = self.gemini_model.generate_content(prompt)
            analysis_text = response.text
            
            # Parse the response
            analysis = self._parse_analysis_response(analysis_text)
            analysis['transcript'] = transcript
            analysis['raw_analysis'] = analysis_text
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing transcript: {e}")
            return self._fallback_analysis(transcript)
    
    def _parse_analysis_response(self, analysis_text: str) -> Dict[str, Any]:
        """
        Parse Gemini analysis response
        
        Args:
            analysis_text: Raw analysis text from Gemini
        
        Returns:
            Parsed analysis dictionary
        """
        analysis = {
            'confidence_score': 5,
            'ai_experience_score': 5,
            'education_status': 'unknown',
            'communication_score': 5,
            'detailed_analysis': analysis_text
        }
        
        try:
            lines = analysis_text.split('\n')
            
            for line in lines:
                line = line.strip()
                
                if 'Confidence Score:' in line:
                    score = self._extract_score(line)
                    if score is not None:
                        analysis['confidence_score'] = score
                
                elif 'AI Experience Score:' in line:
                    score = self._extract_score(line)
                    if score is not None:
                        analysis['ai_experience_score'] = score
                
                elif 'Education Status:' in line:
                    status = line.split(':', 1)[1].strip().lower()
                    analysis['education_status'] = status
                
                elif 'Communication Score:' in line:
                    score = self._extract_score(line)
                    if score is not None:
                        analysis['communication_score'] = score
        
        except Exception as e:
            print(f"Error parsing analysis: {e}")
        
        return analysis
    
    def _extract_score(self, line: str) -> int:
        """Extract numeric score from line"""
        try:
            # Look for pattern like "X/10" or "X"
            import re
            match = re.search(r'(\d+)(?:/10)?', line)
            if match:
                score = int(match.group(1))
                return min(max(score, 1), 10)  # Clamp between 1-10
        except:
            pass
        return None
    
    def _fallback_analysis(self, transcript: str) -> Dict[str, Any]:
        """
        Fallback analysis when Gemini is not available
        
        Args:
            transcript: Transcribed text
        
        Returns:
            Basic analysis results
        """
        # Simple keyword-based analysis
        ai_keywords = ['ai', 'machine learning', 'ml', 'data science', 'python', 
                      'programming', 'algorithm', 'neural network', 'deep learning']
        
        education_keywords = ['graduated', 'final year', 'bachelor', 'master', 
                           'degree', 'university', 'college']
        
        confidence_indicators = ['confident', 'experience', 'expertise', 'skills', 
                               'knowledge', 'proficient']
        
        transcript_lower = transcript.lower()
        
        # Count AI-related mentions
        ai_mentions = sum(1 for keyword in ai_keywords if keyword in transcript_lower)
        ai_score = min(ai_mentions * 2, 10)
        
        # Check education status
        education_status = 'unknown'
        if any(keyword in transcript_lower for keyword in ['graduated', 'graduate']):
            education_status = 'graduated'
        elif any(keyword in transcript_lower for keyword in ['final year', 'last year']):
            education_status = 'final year'
        
        # Basic confidence scoring
        confidence_mentions = sum(1 for keyword in confidence_indicators 
                               if keyword in transcript_lower)
        confidence_score = min(confidence_mentions + 3, 10)
        
        return {
            'confidence_score': confidence_score,
            'ai_experience_score': ai_score,
            'education_status': education_status,
            'communication_score': 5,  # Default score
            'detailed_analysis': f"Basic analysis: AI mentions: {ai_mentions}, "
                               f"Confidence indicators: {confidence_mentions}",
            'transcript': transcript
        }
    
    def analyze_video_complete(self, video_path: str) -> Dict[str, Any]:
        """
        Complete video analysis pipeline
        
        Args:
            video_path: Path to video file
        
        Returns:
            Complete analysis results
        """
        # Step 1: Transcribe video
        transcript = self.transcribe_video(video_path)
        
        if not transcript:
            return {
                'success': False,
                'error': 'Failed to transcribe video',
                'transcript': '',
                'analysis': {}
            }
        
        # Step 2: Analyze transcript
        analysis = self.analyze_transcript(transcript)
        
        return {
            'success': True,
            'transcript': transcript,
            'analysis': analysis,
            'video_path': video_path
        }
