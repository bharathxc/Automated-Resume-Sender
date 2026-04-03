import os
import csv
import smtplib
import time
from datetime import datetime
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
CSV_FILE = "contacts.csv"

def send_emails():
    print("--- Starting Application Script ---")
    
    if not os.path.exists(CSV_FILE):
        print(f"❌ Error: {CSV_FILE} not found!")
        return

    # 1. Load Data
    contacts = []
    try:
        with open(CSV_FILE, 'r', newline='') as file:
            reader = csv.DictReader(file)
            contacts = list(reader)
        print(f"DEBUG: Loaded {len(contacts)} rows from CSV.")
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    # 2. Start Mail Server
    try:
        print("DEBUG: Connecting to Gmail...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            print("✅ Login Successful!")

            for row in contacts:
                company = row.get('Company', 'Unknown')
                email = row.get('Email', '')
                status = str(row.get('Status', '')).strip().lower()

                if status == 'sent' or status == 'followed up':
                    print(f"⏭️ Skipping {company} (Already processed)")
                    continue
                
                if not email:
                    print(f"⚠️ Skipping {company} (No Email)")
                    continue

                # 3. Build and Send 
                msg = EmailMessage()
                msg['Subject'] = f"Internship Application - {company}"
                msg['From'] = EMAIL_USER
                msg['To'] = email

                with open("template.txt", "r") as f:
                    body = f.read().format(Company=company)
                msg.set_content(body)

                # Attach Resume [cite: 1-55]
                with open("resume.pdf", "rb") as f:
                    msg.add_attachment(f.read(), maintype="application", 
                                       subtype="pdf", filename="Bharath_Pradeep_Resume.pdf")

                smtp.send_message(msg)
                print(f"🚀 SUCCESS: Mail sent to {company}")
                
                # Update status and timestamp for the follow-up logic
                row['Status'] = 'Sent'
                row['Date_Sent'] = datetime.now().strftime('%Y-%m-%d')
                time.sleep(2)

        # 4. Save Updates back to CSV
        try:
            with open(CSV_FILE, 'w', newline='') as file:
                # Ensure these headers match exactly
                fieldnames = ['Company', 'Email', 'Status', 'Date_Sent']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(contacts)
                print("✅ CSV updated successfully with date tracking.")
        except PermissionError:
            print("❌ ERROR: Could not save! Please close 'contacts.csv' and run again.")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    send_emails()