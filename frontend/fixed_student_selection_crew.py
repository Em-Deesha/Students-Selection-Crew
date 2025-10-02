"""
Fixed Student Selection Crew - Works with your existing Google Sheet structure
"""
from crewai import Crew, Process
from typing import List, Dict, Any, Optional
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
                existing_data = self.sheets_manager.read_sheet('Students', 'A1:K1')
                if not existing_data or existing_data[0] != headers:
                    # Update headers if needed
                    self.sheets_manager.write_sheet('Students', [headers], 'A1')
                    print("✅ Updated sheet headers")
                else:
                    print("✅ Sheet headers already correct")
            except Exception as e:
                print(f"⚠️ Could not check headers: {e}")
                
        except Exception as e:
            print(f"Error initializing sheet: {e}")
    
    def _auto_shortlist_students(self, results: List[Dict[str, Any]], student_answers: List[Dict[str, Any]] = None) -> None:
        """
        Automatically shortlist top students and send emails
        
        Args:
            results: List of evaluation results
            student_answers: Original student data with emails
        """
        try:
            # Sort students by percentage (descending)
            sorted_students = sorted(results, key=lambda x: x['percentage'], reverse=True)
            
            # Get top 10 students
            top_students = sorted_students[:10]
            
            print(f"🏆 Shortlisting top {len(top_students)} students...")
            
            # Create Shortlisted_Students sheet and add shortlisted students
            self._create_shortlisted_students_sheet()
            
            # Add shortlisted students to Shortlisted_Students sheet
            for i, student in enumerate(top_students):
                # Get email from original student data if not in result
                student_email = student.get('email', '')
                if not student_email and student_answers:
                    for orig_student in student_answers:
                        if orig_student.get('name') == student['student_name']:
                            student_email = orig_student.get('email', '')
                            break
                
                # Add email to student data for email sending
                student['email'] = student_email
                
                # Add to Shortlisted_Students sheet
                self._add_to_shortlisted_sheet(student)
                
                # Send email notification
                if student_email:
                    self._send_shortlist_email(student)
                    print(f"📧 Email sent to {student['student_name']} ({student_email})")
                else:
                    print(f"⚠️ No email for {student['student_name']}")
            
            print(f"✅ Successfully shortlisted {len(top_students)} students!")
            
        except Exception as e:
            print(f"❌ Error in auto-shortlisting: {e}")
    
    def _create_shortlisted_students_sheet(self) -> bool:
        """
        Create Shortlisted_Students sheet with proper headers
        
        Returns:
            True if successful
        """
        try:
            headers = [['Student_ID', 'Student_Name', 'Email', 'Quiz_Score', 'Status',
                       'Student_Answers', 'Video_Link', 'Transcript', 'Confidence', 'AI_Experience', 'Final_Result']]
            self.sheets_manager.write_sheet('Shortlisted_Students', headers, 'A1')
            print("✅ Created Shortlisted_Students sheet with headers")
            return True
        except Exception as e:
            print(f"❌ Error creating Shortlisted_Students sheet: {e}")
            return False
    
    def _add_to_shortlisted_sheet(self, student: Dict[str, Any]) -> None:
        """
        Add student to Shortlisted_Students sheet
        
        Args:
            student: Student data to add
        """
        try:
            # Get existing data to find next row
            existing_data = self.sheets_manager.read_sheet('Shortlisted_Students', 'A:K')
            next_row = len(existing_data) + 1 if existing_data else 2
            
            # Format the quiz score properly
            quiz_score = f"{student['total_score']}/{student['max_possible']} ({student['percentage']:.1f}%)"
            
            # Create student data for shortlisted sheet
            student_data = [
                student.get('student_id', ''),
                student.get('student_name', ''),
                student.get('email', ''),
                quiz_score,
                'Shortlisted',
                '',  # Student answers (not needed in shortlisted sheet)
                '',  # Video Link
                '',  # Transcript
                '',  # Confidence
                '',  # AI Experience
                ''   # Final Result
            ]
            
            # Write to Shortlisted_Students sheet
            self.sheets_manager.write_sheet('Shortlisted_Students', [student_data], f'A{next_row}')
            print(f"✅ Added {student.get('student_name', 'Unknown')} to Shortlisted_Students sheet")
            
        except Exception as e:
            print(f"❌ Error adding student to shortlisted sheet: {e}")
    
    def _update_student_status(self, student_name: str, status: str) -> None:
        """
        Update student status in Students sheet
        
        Args:
            student_name: Name of the student
            status: New status
        """
        try:
            # Read current data
            students_data = self.sheets_manager.read_sheet('Students', 'A:K')
            
            # Find and update the student's status
            for i, row in enumerate(students_data):
                if len(row) > 1 and row[1] == student_name:  # Check student name in column B
                    # Update status (column E - index 4)
                    if len(row) > 4:
                        row[4] = status
                    else:
                        # Extend row to have enough columns
                        while len(row) < 11:  # Ensure we have all 11 columns
                            row.append('')
                        row[4] = status
                    
                    # Write back to sheet
                    self.sheets_manager.write_sheet('Students', [row], f'A{i+1}')
                    break
                    
        except Exception as e:
            print(f"❌ Error updating student status: {e}")
    
    def _send_shortlist_email(self, student: Dict[str, Any]) -> None:
        """
        Send shortlist email to student
        
        Args:
            student: Student information
        """
        try:
            subject = "🎉 Congratulations! You've been shortlisted for the next round"
            
            # Create congratulatory message without specific scores
            score_text = "Your quiz performance was excellent!"
            
            # Get Google Drive folder link
            drive_link = "https://drive.google.com/drive/folders/12N7a6lFq71rRQfuBaF_OBB1mMqHQtYo1?usp=sharing"
            
            # Get student identification for unique video naming
            student_name = student.get('student_name', 'Student').replace(' ', '_')
            student_id = student.get('student_id', 'UNKNOWN')
            video_filename = f"{student_id}_{student_name}_Video.mp4"
            
            body = f"""
Dear {student.get('student_name', 'Student')},

Congratulations! 🎉

You have been shortlisted for the next round of our selection process. 
{score_text}

Next Steps:
📹 Please record a 1-minute video interview answering the following questions:
1. Tell us about yourself and your background
2. Why are you interested in this program?
3. What are your career goals?
4. Any questions you have for us?

📤 Upload your video here: {drive_link}

**CRITICAL INSTRUCTIONS:**
🔸 Your video filename MUST be: {video_filename}
🔸 Student ID: {student_id}
🔸 This ensures we can identify your video correctly

Deadline: 7 days from today

We look forward to seeing your video!

Best regards,
The Selection Committee
            """
            
            # Send email using the email manager
            success = self.email_manager.send_email(
                to_email=student.get('email', ''),
                subject=subject,
                body=body
            )
            
            if success:
                print(f"✅ Email sent successfully to {student.get('student_name', 'Unknown')} ({student.get('email', 'No email')})")
            else:
                print(f"❌ Failed to send email to {student.get('student_name', 'Unknown')} ({student.get('email', 'No email')})")
            
        except Exception as e:
            print(f"❌ Error sending email to {student['student_name']}: {e}")

    def _create_students_sheet(self) -> bool:
        """
        Create Students sheet with proper headers
        
        Returns:
            True if successful
        """
        try:
            # Use the new Students sheet
            headers = [['Student_ID', 'Student_Name', 'Email', 'Quiz_Score', 'Status',
                       'Student_Answers', 'Video_Link', 'Transcript', 'Confidence', 'AI_Experience', 'Final_Result']]
            self.sheets_manager.write_sheet('Students', headers, 'A1')
            print("✅ Created Students sheet with headers")
            return True
        except Exception as e:
            print(f"❌ Error creating Students sheet: {e}")
            return False

    def _create_quiz_questions_sheet(self) -> bool:
        """
        Create Quiz_Questions sheet with proper headers
        
        Returns:
            True if successful
        """
        try:
            # Use the new Quiz_Questions sheet
            headers = [['Question', 'Option_A', 'Option_B', 'Option_C', 'Option_D',
                       'Correct_Answer', 'Points', 'Category', 'Category', 'Difficulty']]
            self.sheets_manager.write_sheet('Quiz_Questions', headers, 'A1')
            print("✅ Created Quiz_Questions sheet with headers")
            return True
        except Exception as e:
            print(f"❌ Error creating Quiz_Questions sheet: {e}")
            return False
    
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
            # Create Quiz_Questions sheet first
            self._create_quiz_questions_sheet()
            
            # Store quiz questions in Quiz_Questions sheet
            quiz_headers = ['Question', 'Option_A', 'Option_B', 'Option_C', 'Option_D', 
                           'Correct_Answer', 'Points', 'Category', 'Category', 'Difficulty']
            
            rows = [quiz_headers]
            
            for i, question in enumerate(questions_data):
                row = [
                    question['question'],  # Question
                    question['options'][0] if len(question['options']) > 0 else '',  # Option_A
                    question['options'][1] if len(question['options']) > 1 else '',  # Option_B
                    question['options'][2] if len(question['options']) > 2 else '',  # Option_C
                    question['options'][3] if len(question['options']) > 3 else '',  # Option_D
                    question['correct_answer'],  # Correct_Answer
                    question['points'],  # Points
                    question['category'],  # Category
                    question['category'],  # Category (duplicate)
                    'Medium'  # Difficulty (default)
                ]
                rows.append(row)
            
            # Write to Quiz_Questions sheet
            self.sheets_manager.write_sheet('Quiz_Questions', rows, 'A1')
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
            # Get quiz questions from Quiz_Questions sheet
            try:
                quiz_data = self.sheets_manager.read_sheet('Quiz_Questions', 'A:J')
            except Exception as e:
                print(f"❌ Quiz_Questions sheet not found: {e}")
                print("📝 Creating Quiz_Questions sheet...")
                self._create_quiz_questions_sheet()
                quiz_data = self.sheets_manager.read_sheet('Quiz_Questions', 'A:J')
            
            if not quiz_data or len(quiz_data) < 2:
                print("❌ No quiz questions found. Please create quiz questions first.")
                return []
            
            # Parse quiz questions
            quiz_questions = []
            for row in quiz_data[1:]:  # Skip header
                if len(row) >= 8:
                    question = {
                        'question': row[0],  # Question is in column A
                        'options': [row[1], row[2], row[3], row[4]],  # Options are in columns B-E
                        'correct_answer': row[5] if row[5] in 'ABCD' else 'A',  # Correct answer is in column F
                        'points': int(row[6]) if str(row[6]).isdigit() else 1,  # Points are in column G
                        'category': row[7]  # Category is in column H
                    }
                    quiz_questions.append(question)
            
            # Evaluate answers
            print(f"🔍 Debug - Evaluating {len(student_answers)} students with {len(quiz_questions)} questions")
            for student in student_answers:
                print(f"  Student: {student['name']}, Answers: {student['answers']}")
            
            try:
                results = self.checker.evaluate_answers(student_answers, quiz_questions)
                print(f"🔍 Debug - Evaluation results: {len(results) if results else 0} results")
            except Exception as e:
                print(f"❌ Error during evaluation: {e}")
                return []
            
            # Store results in separate sheets for better organization
            if results:
                print(f"📊 Storing {len(results)} student results...")
                
                # Create/Update Students sheet
                self._create_students_sheet()
                
                # Get existing student data to check for duplicates
                try:
                    existing_students = self.sheets_manager.read_sheet('Students', 'A:K')
                    existing_emails = set()
                    if existing_students and len(existing_students) > 1:  # Skip header row
                        for row in existing_students[1:]:  # Skip header
                            if len(row) > 2 and row[2]:  # Check if email exists
                                existing_emails.add(row[2].strip().lower())
                except:
                    existing_emails = set()
                
                # Store student data in Students sheet (only if not duplicate)
                new_students = []
                for i, result in enumerate(results):
                    # Get email from the original student data
                    student_email = ''
                    for student in student_answers:
                        if student['name'] == result['student_name']:
                            student_email = student.get('email', '')
                            break
                    
                    # Check if this student already exists
                    if student_email and student_email.strip().lower() in existing_emails:
                        print(f"⚠️ Skipping duplicate student: {result['student_name']} ({student_email})")
                        continue
                    
                    # Get the original answers for this student
                    original_answers = []
                    for student in student_answers:
                        if student.get('name') == result['student_name'] or student.get('email') == student_email:
                            original_answers = student.get('answers', [])
                            break
                    
                    # Format answers as comma-separated string
                    answers_str = ','.join(original_answers) if original_answers else ''
                    
                    # Format the quiz score properly
                    quiz_score = f"{result['total_score']}/{result['max_possible']} ({result['percentage']:.1f}%)"
                    
                    student_data = [
                        result['student_id'],
                        result['student_name'],
                        student_email,
                        quiz_score,  # Properly formatted quiz score
                        'Quiz Completed',
                        answers_str,  # Store the actual answers
                        '',  # Video Link
                        '',  # Transcript
                        '',  # Confidence
                        '',  # AI Experience
                        ''   # Final Result
                    ]
                    
                    new_students.append(student_data)
                
                # Write all new students at once
                if new_students:
                    try:
                        existing_students = self.sheets_manager.read_sheet('Students', 'A:K')
                        next_row = len(existing_students) + 1 if existing_students else 2
                    except:
                        next_row = 2
                    
                    for i, student_data in enumerate(new_students):
                        row_num = next_row + i
                        print(f"📝 Writing student {student_data[1]} to Students row {row_num}")
                        # Write to Students sheet
                        self.sheets_manager.write_sheet('Students', [student_data], f'A{row_num}')
                    
                    print(f"✅ Successfully stored {len(new_students)} new student results in Students sheet!")
                else:
                    print("ℹ️ No new students to add (all were duplicates)")
                
                # Automatically shortlist top students and send emails
                self._auto_shortlist_students(results, student_answers)
            
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
            # Get student data from Students sheet (READ ONLY - NO MODIFICATIONS)
            student_data = self.sheets_manager.read_sheet('Students', 'A:K')
            
            if not student_data or len(student_data) < 2:
                print("❌ No student data found. Please evaluate quiz submissions first.")
                return []
            
            # Parse student results (READ ONLY)
            students = []
            for row in student_data[1:]:  # Skip header
                if len(row) >= 4 and row[3]:  # Has quiz score in column D
                    # Parse quiz score (e.g., "3/4 (75.0%)")
                    quiz_score = row[3]
                    if '/' in quiz_score:
                        try:
                            score_parts = quiz_score.split('/')[0]
                            total_score = float(score_parts)
                        except:
                            total_score = 0
                    else:
                        total_score = 0
                    
                    student = {
                        'student_id': row[0] if len(row) > 0 else f"STU{len(students)+1:03d}",
                        'student_name': row[1] if len(row) > 1 else '',
                        'email': row[2] if len(row) > 2 else '',
                        'total_score': total_score,
                        'percentage': total_score * 25 if total_score > 0 else 0  # Assuming 4 questions
                    }
                    students.append(student)
            
            if not students:
                print("❌ No students with quiz results found")
                return []
            
            # Sort by score and select top students
            students.sort(key=lambda x: x['total_score'], reverse=True)
            shortlisted = students[:Config.MAX_SHORTLIST]
            
            # Create Shortlisted_Students sheet and add students (NO MODIFICATION TO STUDENTS SHEET)
            self._create_shortlisted_students_sheet()
            
            # Add shortlisted students to Shortlisted_Students sheet
            for student in shortlisted:
                self._add_to_shortlisted_sheet(student)
            
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
                    student_data = self.sheets_manager.read_sheet('Students', 'A:K')
                    
                    for i, row in enumerate(student_data[1:], 2):  # Skip header, start from row 2
                        if len(row) >= 1 and row[0]:  # Has student name
                            # Update video analysis data
                            if result['success']:
                                self.sheets_manager.update_cell('Students', f'G{i}', 'Video Uploaded')
                                self.sheets_manager.update_cell('Students', f'H{i}', result['transcript'][:100] + '...')
                                self.sheets_manager.update_cell('Students', f'I{i}', str(result['confidence_score']))
                                self.sheets_manager.update_cell('Students', f'J{i}', str(result['ai_experience_score']))
                            
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
            # Get student data from Shortlisted_Students sheet where video analysis is stored
            student_data = self.sheets_manager.read_sheet('Shortlisted_Students', 'A:K')
            
            if not student_data or len(student_data) < 2:
                print("❌ No shortlisted student data found.")
                return []
            
            print(f"📊 Found {len(student_data)-1} shortlisted students")
            
            # Parse students with video analysis
            # Columns: A=Student_ID, B=Student_Name, C=Email, D=Quiz_Score, E=Status, 
            # F=Student_Answers, G=Video_Link, H=Transcript, I=Confidence, J=AI_Experience, K=Final_Result
            candidates = []
            for row in student_data[1:]:  # Skip header
                if len(row) >= 10:  # Must have at least confidence and AI experience data
                    video_link = row[6] if len(row) > 6 else None
                    transcript = row[7] if len(row) > 7 else None
                    confidence = row[8] if len(row) > 8 else None
                    ai_experience = row[9] if len(row) > 9 else None
                    
                    # Only include students with video analysis completed
                    if video_link and transcript and confidence and ai_experience:
                        try:
                            confidence_score = float(confidence) if confidence and str(confidence).replace('.', '').replace('-', '').isdigit() else 0
                            ai_experience_score = float(ai_experience) if ai_experience and str(ai_experience).replace('.', '').replace('-', '').isdigit() else 0
                            
                            candidate = {
                                'student_id': row[0] if len(row) > 0 else f"STU{len(candidates)+1:03d}",
                                'student_name': row[1] if len(row) > 1 else 'Unknown',
                                'email': row[2] if len(row) > 2 else 'unknown@email.com',
                                'quiz_score': row[3] if len(row) > 3 else 'N/A',
                                'confidence_score': confidence_score,
                                'ai_experience_score': ai_experience_score,
                                'communication_score': ai_experience_score * 0.9,  # Estimate from AI experience
                                'video_file': video_link,
                                'transcript_length': len(transcript) if transcript else 0,
                                'education_status': 'graduated',  # Default
                                'success': True  # Mark as successful analysis
                            }
                            candidates.append(candidate)
                            print(f"✅ Added candidate: {candidate['student_name']} (Confidence: {confidence_score}, AI Experience: {ai_experience_score})")
                        except (ValueError, TypeError) as e:
                            print(f"⚠️ Skipping {row[1] if len(row) > 1 else 'Unknown'}: Invalid scores - {e}")
                    else:
                        print(f"⚠️ Skipping {row[1] if len(row) > 1 else 'Unknown'}: Missing video analysis data")
            
            if not candidates:
                print("❌ No candidates with video analysis found")
                return []
            
            # Select final candidates
            final_candidates = self.finalizer.select_final_candidates(candidates)
            
            # Update final results in Shortlisted_Students sheet
            for candidate in final_candidates:
                # Find the candidate in the sheet and update final result
                for j, row in enumerate(student_data[1:], 2):
                    if len(row) >= 2 and row[1] == candidate['student_name']:
                        # Update Final_Result column (K) with 'Selected'
                        self.sheets_manager.update_cell('Shortlisted_Students', f'K{j}', 'Selected')
                        print(f"✅ Updated {candidate['student_name']} status to 'Selected'")
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
            student_data = self.sheets_manager.read_sheet('Students', 'A:K')
            
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
            
            # Count quiz questions
            quiz_questions = 0
            try:
                quiz_data = self.sheets_manager.read_sheet('Quiz_Questions', 'A:J')
                if quiz_data and len(quiz_data) > 1:
                    for row in quiz_data[1:]:
                        if len(row) >= 8 and row[0]:  # Has question data
                            quiz_questions += 1
            except:
                quiz_questions = 0
            
            return {
                'quiz_questions': quiz_questions,
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
