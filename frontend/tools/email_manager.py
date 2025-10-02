"""
Email management tool for sending notifications
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import os

class EmailManager:
    def __init__(self, username: str, password: str):
        """
        Initialize email manager
        
        Args:
            username: Gmail username
            password: Gmail app password
        """
        self.username = username
        self.password = password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """
        Send email to a single recipient
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body
        
        Returns:
            True if successful, False otherwise
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            
            text = msg.as_string()
            server.sendmail(self.username, to_email, text)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_bulk_emails(self, recipients: List[Dict[str, str]]) -> Dict[str, bool]:
        """
        Send emails to multiple recipients
        
        Args:
            recipients: List of dicts with 'email', 'subject', 'body' keys
        
        Returns:
            Dict mapping email addresses to success status
        """
        results = {}
        
        for recipient in recipients:
            email = recipient['email']
            subject = recipient['subject']
            body = recipient['body']
            
            success = self.send_email(email, subject, body)
            results[email] = success
        
        return results
    
    def send_shortlist_notification(self, email: str, drive_link: str, deadline: str) -> bool:
        """
        Send shortlist notification email
        
        Args:
            email: Recipient email
            drive_link: Google Drive link for video upload
            deadline: Submission deadline
        
        Returns:
            True if successful
        """
        subject = "Congratulations! You've been shortlisted"
        body = f"""
Congratulations! You have been shortlisted for the next round.

Please upload a 1-minute video interview at the following link:
{drive_link}

The video should cover:
- Your background and experience
- Why you're interested in AI/ML
- Your current education status

Deadline: {deadline}

Best regards,
Student Selection Team
        """
        
        return self.send_email(email, subject, body)
    
    def send_final_selection_notification(self, email: str) -> bool:
        """
        Send final selection notification email
        
        Args:
            email: Recipient email
        
        Returns:
            True if successful
        """
        subject = "🎉 Congratulations! You've been selected for AgenticAI Course"
        body = """
Dear Student,

🎉 Congratulations! 

You have been selected for the AgenticAI course! 

We were impressed by your quiz performance and video interview. Your dedication and skills have earned you a spot in our program.

📚 Course details will be shared with you shortly via email.

We're excited to have you join our AgenticAI learning community!

Best regards,
AgenticAI Selection Team
        """
        
        return self.send_email(email, subject, body)
