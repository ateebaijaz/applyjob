from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

SENDER_EMAIL = os.getenv("GMAIL_USER")
SENDER_PASSWORD = os.getenv("GMAIL_PASS")

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/send-email")
async def send_email(
    request: Request,
    email_id: str = Form(...),
    receiver_name: str = Form(...),
    position: str = Form(...),
    linkedin: str = Form(...),
    github: str = Form(...)
):
    subject = f"Applying for {position}"
    greeting = f"Hi {receiver_name}," if receiver_name.strip() else "Dear Hiring Manager,"

    body = f"""
{greeting}

I am writing to express my interest in the {position} role. With 5 years of hands-on experience in building robust, scalable backend systems using Python and Django I bring a solid understanding of microservices architecture, cloud infrastructure (AWS & Azure), and API development.

{add_your_experience}

My current CTC is XX LPA, and my last working day is 2nd June 2025. I am actively seeking my next opportunity where I can contribute to impactful backend systems and continue growing technically.

Please find my resume attached. I look forward to the opportunity to discuss how my experience and skills align with your team’s needs.

Best regards,  
xxxxxxxxx  
📞 +91 XXXXXXXXXXX  
📧 XXXX@gmail.com  
🔗 LinkedIn: {linkedin}  
🔗 GitHub: {github}
"""

    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = email_id
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with open("Resume.pdf", "rb") as file:
            part = MIMEApplication(file.read(), Name="Resume.pdf")
            part['Content-Disposition'] = 'attachment; filename="Resume.pdf"'
            message.attach(part)
    except FileNotFoundError:
        return templates.TemplateResponse("form.html", {"request": request, "status": "Resume file not found!"})

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(message)
        status = "✅ Email sent successfully!"
    except Exception as e:
        status = f"Error sending email: {str(e)}"

    return templates.TemplateResponse("form.html", {"request": request, "status": status})
