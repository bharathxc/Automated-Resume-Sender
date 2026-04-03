import os
import csv
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
CSV_FILE = "contacts.csv"

def send_followups():
    contacts = []
    with open(CSV_FILE, 'r', newline='') as file:
        reader = csv.DictReader(file)
        contacts = list(reader)

    today = datetime.now()
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)

        for row in contacts:
            # Only follow up if it was sent and hasn't been followed up yet
            if row['Status'] == 'Sent' and row.get('Date_Sent'):
                sent_date = datetime.strptime(row['Date_Sent'], '%Y-%m-%d')
                
                # Check if 7 days have passed
                if today >= sent_date + timedelta(days=7):
                    print(f"📧 Sending follow-up to {row['Company']}...")
                    
                    msg = EmailMessage()
                    msg['Subject'] = f"Following up: Internship Application - {row['Company']}"
                    msg['From'] = EMAIL_USER
                    msg['To'] = row['Email']
                    
                    body = f"Hi Team at {row['Company']},\n\nI'm following up on my internship application sent last week. I remain very interested in the role and would love to discuss how my skills in Data Science can contribute to your team. Please let me know if there is anything i can do to stand out or even help your team in any way. \n\nBest regards,\nBharath"
                    msg.set_content(body)

                    try:
                        smtp.send_message(msg)
                        row['Status'] = 'Followed Up'
                        print(f"🚀 Follow-up successful for {row['Company']}")
                    except Exception as e:
                        print(f"❌ Failed: {e}")

    # Save changes
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Company', 'Email', 'Status', 'Date_Sent'])
        writer.writeheader()
        writer.writerows(contacts)

if __name__ == "__main__":
    send_followups()