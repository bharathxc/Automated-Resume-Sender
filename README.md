# Automated-Resume-Sender
This project helps with sending your resume in mail with a subject and body automatically to companies where you only have to input the mails of the companies.
🤖 Autonomous Procurement & Email Automation Agent
This project is a specialized module within an AI-driven Inventory Management System. It serves as the "Communication Brain," automatically drafting and dispatching strategic negotiation emails to vendors when the system detects a critical stockout risk.

🌟 Key Features
Metric-Driven Drafting: The agent doesn't use static templates. It ingests real-time data—including Revenue at Risk, Predicted Shortfall, and Current Market Price—to customize the message.

Dynamic Negotiation Logic: Implements a tiered "ask" strategy. If the financial risk exceeds a specific threshold, the agent automatically pivots to a high-leverage negotiation tone (e.g., requesting a 15% bulk discount).

Secure SMTP Integration: Utilizes Python’s smtplib and EmailMessage protocols to send high-priority alerts via Gmail’s SSL-secured SMTP servers.

Human-in-the-Loop Workflow: Designed for a Streamlit-based dashboard, allowing a warehouse manager to review, edit, and approve AI-generated drafts before they are dispatched.

🛠️ Technical Stack
Language: Python 3.x

Communication: smtplib, email.message

Security: App-Specific Password (ASP) integration with SSL (Port 465)

Dashboard Integration: Built for seamless use with Streamlit st.text_area and st.button components.

📂 Module Structure
Bash
├── negotiation_agent.py   # Core logic for drafting and sending emails
├── dashboard.py           # UI layer for reviewing AI drafts
└── .env                   # (Optional) Secure storage for credentials
🚀 How it Works
Risk Detection: The main inventory engine identifies a product where current_stock <= reorder_point.

Payload Generation: The system calculates the shortfall (units needed) and the revenue_at_risk (potential loss if not restocked).

The Draft: draft_negotiation_email() creates a professional inquiry, including specific data points to give the warehouse leverage in the conversation.

Secure Dispatch: Once approved, send_negotiation_email() connects to the SMTP server and delivers the request to the vendor's inbox.

⚙️ Setup & Configuration
To use the automated email feature, you must have 2-Step Verification enabled on your Google Account:

Generate an App Password: Go to your Google Account Security settings and create a 16-character "App Password."

Update Credentials: Update the sender_email and app_password variables in negotiation_agent.py.

Port Configuration: The system uses SMTP_SSL on Port 465 for maximum security.

📈 Future Enhancements (DS/ML Roadmap)
NLP Sentiment Analysis: Use Hugging Face Transformers to analyze vendor replies and suggest the next best negotiation step.

LLM Integration: Integrate Ollama (Llama 3) to generate highly nuanced, non-templated negotiation strategies based on historical vendor performance.

Attachment Support: Automatically attach CSV "Demand Forecast Reports" to emails to prove the urgency to the vendor.
