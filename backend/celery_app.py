from celery import Celery
from celery.schedules import crontab
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import csv
import io
import os
from datetime import datetime, timedelta
import redis

celery = Celery(
    'quiz_master',
    broker='redis://localhost:6379',
    backend='redis://localhost:6379',
    include=['celery_app']
)

celery.conf.update(
    timezone='UTC',
    beat_schedule={
        'daily-reminders': {
            'task': 'celery_app.send_daily_reminders',
            'schedule': crontab(hour=5, minute=19),
        },
        'monthly-reports': {
            'task': 'celery_app.send_monthly_reports',
            'schedule': crontab(hour=5, minute=19),
        },
    }
)

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'saarthakmainiofficial@gmail.com'
EMAIL_PASSWORD = 'mcuu lemx gnvd fllt'

def send_email(to_email, subject, body, attachment=None):
    """Send email with optional attachment"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))
        
        if attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment['data'])
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {attachment["filename"]}'
            )
            msg.attach(part)
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, to_email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@celery.task
def send_daily_reminders():
    """Send daily reminders to inactive users"""

    import sys
    import os

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from models import User, Quiz
    from app import app
    from database import db

    with app.app_context():
        cutoff_date = datetime.utcnow() - timedelta(days=3)
        inactive_users = User.query.filter(
            User.role == 'user',
            User.last_login < cutoff_date
        ).all()
        
        recent_quizzes = Quiz.query.filter(
            Quiz.date_of_quiz >= datetime.utcnow() - timedelta(days=7),
            Quiz.is_active == True
        ).all()
        
        for user in inactive_users:
            subject = "Don't Miss Out on New Quizzes!"
            
            quiz_list = ""
            for quiz in recent_quizzes[:5]:
                quiz_list += f"""
                <li style="margin: 10px 0;">
                    <strong>{quiz.title}</strong><br>
                    <small style="color: #666;">
                        {quiz.chapter.subject.name} - {quiz.chapter.name} | 
                        {quiz.time_duration} minutes
                    </small>
                </li>
                """
            
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #007bff;">Hello {user.full_name}! </h2>
                    
                    <p>We noticed you haven't visited Quiz Master recently. We have some exciting new quizzes waiting for you!</p>
                    
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                        <h3 style="color: #28a745; margin-top: 0;">Recent Quizzes:</h3>
                        <ul style="padding-left: 20px;">
                            {quiz_list if quiz_list else '<li>No new quizzes this week</li>'}
                        </ul>
                    </div>
                    
                    <p>Don't let your skills get rusty! Log in now and challenge yourself with these quizzes.</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://localhost:5173/login" 
                           style="background: #007bff; color: white; padding: 12px 24px; 
                                  text-decoration: none; border-radius: 5px; display: inline-block;">
                            Start Quiz Now! 
                        </a>
                    </div>
                    
                    <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                    <p style="font-size: 12px; color: #666; text-align: center;">
                        This is an automated reminder from Quiz Master.<br>
                        Keep learning, keep growing! 
                    </p>
                </div>
            </body>
            </html>
            """
            
            # send_email(user.email, subject, body)
            send_email("saarthakmaini@gmail.com", subject, body)
            print(f"Reminder sent to {user.email}")
    
    return f"Daily reminders sent to {len(inactive_users)} users"

@celery.task
def send_monthly_reports():
    """Send monthly activity reports to all users"""

    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from models import db, User, Score
    
    from app import app
    with app.app_context():
        users = User.query.filter_by(role='user').all()
        
        today = datetime.utcnow()
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)
        
        for user in users:
            monthly_scores = Score.query.filter(
                Score.user_id == user.id,
                Score.timestamp_of_attempt >= first_day_last_month,
                Score.timestamp_of_attempt <= last_day_last_month
            ).all()
            
            if not monthly_scores:
                continue
            
            total_quizzes = len(monthly_scores)
            total_score = sum(score.total_scored for score in monthly_scores)
            total_possible = sum(score.total_possible for score in monthly_scores)
            average_percentage = (total_score / total_possible * 100) if total_possible > 0 else 0
            best_score = max(score.percentage for score in monthly_scores)
            
            subject_performance = {}
            for score in monthly_scores:
                subject_name = score.quiz.chapter.subject.name
                if subject_name not in subject_performance:
                    subject_performance[subject_name] = {'count': 0, 'total_percentage': 0}
                subject_performance[subject_name]['count'] += 1
                subject_performance[subject_name]['total_percentage'] += score.percentage
            
            for subject in subject_performance:
                count = subject_performance[subject]['count']
                subject_performance[subject]['average'] = subject_performance[subject]['total_percentage'] / count
            
            subject_report = ""
            for subject, perf in subject_performance.items():
                subject_report += f"""
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #eee;">{subject}</td>
                    <td style="padding: 8px; border-bottom: 1px solid #eee; text-align: center;">{perf['count']}</td>
                    <td style="padding: 8px; border-bottom: 1px solid #eee; text-align: center;">{perf['average']:.1f}%</td>
                </tr>
                """

            if average_percentage >= 90:
                badge = "Outstanding"
                badge_color = "#28a745"
            elif average_percentage >= 80:
                badge = "Excellent"
                badge_color = "#007bff"
            elif average_percentage >= 70:
                badge = "Good"
                badge_color = "#ffc107"
            elif average_percentage >= 60:
                badge = "Average"
                badge_color = "#fd7e14"
            else:
                badge = "Keep Learning"
                badge_color = "#dc3545"
            
            subject = f"Your Monthly Quiz Report - {last_day_last_month.strftime('%B %Y')}"
            
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="text-align: center; background: linear-gradient(135deg, #007bff, #0056b3); 
                                color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px;">
                        <h1 style="margin: 0; font-size: 24px;">Monthly Report</h1>
                        <p style="margin: 10px 0 0 0; opacity: 0.9;">
                            {last_day_last_month.strftime('%B %Y')} Performance Summary
                        </p>
                    </div>
                    
                    <h2 style="color: #333;">Hello {user.full_name}! </h2>
                    
                    <p>Here's your quiz performance summary for {last_day_last_month.strftime('%B %Y')}:</p>

                    <div style="text-align: center; margin: 30px 0;">
                        <div style="background: {badge_color}; color: white; padding: 15px 25px; 
                                    border-radius: 25px; display: inline-block; font-size: 18px; font-weight: bold;">
                            {badge}
                        </div>
                    </div>

                    <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 25px 0;">
                        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; text-align: center;">
                            <div>
                                <h3 style="color: #007bff; margin: 0; font-size: 2em;">{total_quizzes}</h3>
                                <p style="margin: 5px 0 0 0; color: #666;">Quizzes Taken</p>
                            </div>
                            <div>
                                <h3 style="color: #28a745; margin: 0; font-size: 2em;">{average_percentage:.1f}%</h3>
                                <p style="margin: 5px 0 0 0; color: #666;">Average Score</p>
                            </div>
                            <div>
                                <h3 style="color: #ffc107; margin: 0; font-size: 2em;">{best_score:.1f}%</h3>
                                <p style="margin: 5px 0 0 0; color: #666;">Best Score</p>
                            </div>
                            <div>
                                <h3 style="color: #17a2b8; margin: 0; font-size: 2em;">{total_score}/{total_possible}</h3>
                                <p style="margin: 5px 0 0 0; color: #666;">Total Points</p>
                            </div>
                        </div>
                    </div>

                    <h3 style="color: #333; margin-top: 30px;"> Subject-wise Performance:</h3>
                    <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
                        <thead>
                            <tr style="background: #007bff; color: white;">
                                <th style="padding: 12px; text-align: left;">Subject</th>
                                <th style="padding: 12px; text-align: center;">Quizzes</th>
                                <th style="padding: 12px; text-align: center;">Average</th>
                            </tr>
                        </thead>
                        <tbody>
                            {subject_report}
                        </tbody>
                    </table>
                    
                    <div style="background: linear-gradient(135deg, #28a745, #20c997); color: white; 
                                padding: 20px; border-radius: 10px; margin: 30px 0; text-align: center;">
                        <h3 style="margin: 0 0 10px 0;">Keep Going!</h3>
                        <p style="margin: 0;">
                            {"Amazing work this month! Keep up the excellent performance! " if average_percentage >= 80 
                             else "Good progress! Keep practicing to improve your scores! " if average_percentage >= 60
                             else "Every expert was once a beginner. Keep learning and growing!"}
                        </p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://localhost:5173/dashboard" 
                           style="background: #007bff; color: white; padding: 12px 24px; 
                                  text-decoration: none; border-radius: 5px; display: inline-block;">
                            Continue Learning 
                        </a>
                    </div>
                    
                    <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                    <p style="font-size: 12px; color: #666; text-align: center;">
                        This is your automated monthly report from Quiz Master.<br>
                        Generated on {datetime.utcnow().strftime('%B %d, %Y')}
                    </p>
                </div>
            </body>
            </html>
            """
            
            # send_email(user.email, subject, body)
            send_email("saarthakmaini@gmail.com", subject, body)
            print(f"Monthly report sent to {user.email}")
    
    users_with_reports = 0
    for user in users:
        monthly_scores = Score.query.filter(
            Score.user_id == user.id,
            Score.timestamp_of_attempt >= first_day_last_month,
            Score.timestamp_of_attempt <= last_day_last_month
        ).all()
        if monthly_scores:
            users_with_reports += 1
    
    return f"Monthly reports sent to {users_with_reports} users"

@celery.task
def export_user_quiz_data(user_id):
    """Export quiz data for a specific user as CSV"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from models import db, User, Score
    
    # Create Flask app context
    from app import app
    with app.app_context():
        user = User.query.get(user_id)
        if not user:
            return "User not found"
        
        scores = Score.query.filter_by(user_id=user_id).order_by(Score.timestamp_of_attempt.desc()).all()
        
        if not scores:
            return "No quiz data found for user"
        
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow([
            'Quiz ID', 'Quiz Title', 'Subject', 'Chapter', 'Date Taken',
            'Score', 'Total Points', 'Percentage', 'Time Taken (seconds)', 'Remarks'
        ])
        
        for score in scores:
            writer.writerow([
                score.quiz_id,
                score.quiz.title,
                score.quiz.chapter.subject.name,
                score.quiz.chapter.name,
                score.timestamp_of_attempt.strftime('%Y-%m-%d %H:%M:%S'),
                score.total_scored,
                score.total_possible,
                f"{score.percentage:.2f}%",
                score.time_taken,
                score.quiz.remarks or ''
            ])
        
        csv_data = output.getvalue()
        output.close()
        
        subject = "Your Quiz Data Export"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Hello {user.full_name}!</h2>
            <p>Your quiz data export is ready! Please find your quiz history attached as a CSV file.</p>
            
            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <strong>Export Summary:</strong>
                <ul>
                    <li>Total Quiz Attempts: {len(scores)}</li>
                    <li>Export Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</li>
                    <li>File Format: CSV</li>
                </ul>
            </div>
            
            <p>You can open this file in Excel, Google Sheets, or any spreadsheet application.</p>
            
            <p>Happy learning!<br>
            Quiz Master Team</p>
        </body>
        </html>
        """
        
        attachment = {
            'data': csv_data.encode(),
            'filename': f'quiz_data_{user.username}_{datetime.utcnow().strftime("%Y%m%d")}.csv'
        }
        
        send_email(user.email, subject, body, attachment)
        
        return f"Quiz data exported and sent to {user.email}"

@celery.task
def export_admin_quiz_data():
    """Export all quiz data for admin as CSV"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from models import db, User, Score, Quiz

    from app import app
    with app.app_context():
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            return "Admin user not found"
        
        scores = Score.query.order_by(Score.timestamp_of_attempt.desc()).all()
        
        if not scores:
            return "No quiz data found"
        
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow([
            'User ID', 'Username', 'Full Name', 'Quiz ID', 'Quiz Title', 
            'Subject', 'Chapter', 'Date Taken', 'Score', 'Total Points', 
            'Percentage', 'Time Taken (seconds)', 'User Email'
        ])
        
        for score in scores:
            writer.writerow([
                score.user_id,
                score.user.username,
                score.user.full_name,
                score.quiz_id,
                score.quiz.title,
                score.quiz.chapter.subject.name,
                score.quiz.chapter.name,
                score.timestamp_of_attempt.strftime('%Y-%m-%d %H:%M:%S'),
                score.total_scored,
                score.total_possible,
                f"{score.percentage:.2f}%",
                score.time_taken,
                score.user.email
            ])
        
        csv_data = output.getvalue()
        output.close()
        
        subject = "Complete Quiz Data Export"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Quiz Master Admin Report</h2>
            <p>Complete quiz data export is ready! The attached CSV file contains all quiz attempts from all users.</p>
            
            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <strong>Export Summary:</strong>
                <ul>
                    <li>Total Quiz Attempts: {len(scores)}</li>
                    <li>Total Users: {User.query.filter_by(role='user').count()}</li>
                    <li>Total Quizzes: {Quiz.query.count()}</li>
                    <li>Export Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</li>
                    <li>File Format: CSV</li>
                </ul>
            </div>
            
            <p>This file contains comprehensive data for analysis and reporting purposes.</p>
            
            <p>Best regards,<br>
            Quiz Master System</p>
        </body>
        </html>
        """
        
        attachment = {
            'data': csv_data.encode(),
            'filename': f'all_quiz_data_{datetime.utcnow().strftime("%Y%m%d")}.csv'
        }
        
        send_email(admin.email, subject, body, attachment)
        # send_email("saarthakmaini@gmail.com", subject, body, attachment)
        
        return f"Complete quiz data exported and sent to {admin.email}"

if __name__ == '__main__':
    celery.start()