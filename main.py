from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import os
import csv
from io import StringIO

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
    email_id: str = Form(""),
    receiver_name: str = Form(...),
    position: str = Form(...),
    linkedin: str = Form(...),
    github: str = Form(...),
    csv_file: UploadFile = File(None)
):
    results = []

    print(f"Received email_id: {email_id}")
    print(f"milgayeyyyyy   csv_file: {csv_file}")

    def create_email_body(receiver: str):
        greeting = f"Hi {receiver}," if receiver.strip() else "Dear Hiring Manager,"
        return f"""
{greeting}

I am writing to express my interest in the {position} role. With 1.5 years of hands-on experience in building robust, scalable backend systems using Python and Django, I bring a solid understanding of microservices architecture, cloud infrastructure (AWS & Azure), and API development.

My current CTC is XX LPA, and my last working day is 2nd June 2025. I am actively seeking my next opportunity where I can contribute to impactful backend systems and continue growing technically.

Please find my resume attached. I look forward to the opportunity to discuss how my experience and skills align with your team’s needs.

Best regards,  
xxxxxxxxx  
📞 +91 XXXXXXXXXXX  
📧 XXXX@gmail.com  
🔗 LinkedIn: {linkedin}  
🔗 GitHub: {github}
"""

    # Get recipient emails
    recipients = []

    if csv_file and csv_file.filename:
        print(f"Received CSV file: {csv_file.filename}")
        try:
            content = await csv_file.read()
            f = StringIO(content.decode())
            reader = csv.reader(f)
            recipients = [row[0].strip() for row in reader if row and row[0].strip()]
        except Exception as e:
            return templates.TemplateResponse("form.html", {
                "request": request,
                "status": f"Error reading CSV file: {str(e)}"
            })
    elif email_id:
        print(f"Received email_id: {email_id}")
        recipients = [email_id.strip()]
    else:
        return templates.TemplateResponse("form.html", {
            "request": request,
            "status": "Please provide a single email or upload a CSV file."
        })

    for recipient in recipients:
        print(f"Sending email to: {recipient}")
        try:
            message = MIMEMultipart()
            message["From"] = SENDER_EMAIL
            message["To"] = recipient
            message["Subject"] = f"Applying for {position}"
            body = create_email_body(receiver_name)
            message.attach(MIMEText(body, "plain"))

            # Attach resume
            with open("Resume.pdf", "rb") as file:
                part = MIMEApplication(file.read(), Name="Resume.pdf")
                part['Content-Disposition'] = 'attachment; filename="Resume.pdf"'
                message.attach(part)

            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                smtp.starttls()
                smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
                smtp.send_message(message)

            results.append(f"✅ Email sent to {recipient}")
        except Exception as e:
            results.append(f"Failed to send to {recipient}: {str(e)}")

    return templates.TemplateResponse("form.html", {
        "request": request,
        "status": "<br>".join(results)
    })
