# Job Application Email Sender

A FastAPI-based web application that helps you send job application emails with your resume attached. The application provides a simple web interface to input recipient details and automatically sends a formatted email with your resume.

## Features

- Web-based form interface for easy input
- Automated email sending with resume attachment
- Customizable email template
- Secure email handling using environment variables
- Support for Gmail SMTP

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.7 or higher
- pip (Python package installer)

## Required Python Packages

The following packages are required to run this application:
- fastapi
- python-multipart
- jinja2
- python-dotenv
- uvicorn

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your Gmail credentials:
```
GMAIL_USER=your.email@gmail.com
GMAIL_PASS=your_app_password
```

5. Copy your resume in the root folder.

Note: For Gmail, you'll need to use an App Password. To generate one:
1. Enable 2-Step Verification in your Google Account
2. Go to Security → App Passwords
3. Generate a new app password for this application

## Project Structure

```
.
├── main.py              # Main FastAPI application
├── templates/           # HTML templates
│   └── form.html       # Email form template
├── .env                # Environment variables (create this)
└── Resume.pdf          # Your resume file (place this in root directory)
```

## Running the Application

1. Make sure your virtual environment is activated
2. Start the server:
```bash
uvicorn main:app --reload
```
3. Open your browser and navigate to `http://localhost:8000`

## Usage

1. Fill in the form with:
   - Recipient's email address
   - Recipient's name
   - Position you're applying for
   - Your LinkedIn profile URL
   - Your GitHub profile URL

2. Click "Send Email" to send your application

## Security Notes

- Never commit your `.env` file to version control
- Keep your Gmail App Password secure
- Make sure your resume file is named "Resume.pdf" and placed in the root directory

## Troubleshooting

If you encounter any issues:
1. Ensure all required packages are installed
2. Verify your Gmail credentials in the `.env` file
3. Check that your resume file exists and is named correctly
4. Make sure you're using an App Password if you have 2FA enabled

## License

This project is open source and available under the MIT License. 