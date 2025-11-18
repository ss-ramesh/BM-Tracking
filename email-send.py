import smtplib
import ssl
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# -----------------------------------------
# 1. GMAIL SENDER INFORMATION
# -----------------------------------------
GMAIL_ADDRESS = "santosh@boilermake.org"
APP_PASSWORD = "your_16_digit_app_password"  # DO NOT use your real Gmail password

# -----------------------------------------
# 2. FILE PATHS
# -----------------------------------------
CSV_PATH = "Outside Clubs _ Orgs - Sheet1 (1).csv"
EMAIL_DRAFT_PATH = "email-draft.txt"
ATTACHMENT_PATH = "Apps open flyer (1).png"

# -----------------------------------------
# 3. LOAD EMAIL DRAFT
# -----------------------------------------
with open(EMAIL_DRAFT_PATH, "r") as f:
    EMAIL_BODY = f.read()

# -----------------------------------------
# 4. SEND EMAIL FUNCTION
# -----------------------------------------
def send_email(recipient_university, recipient_email, recipient_club):
    msg = MIMEMultipart()
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = recipient_email
    msg["Subject"] = f"Invitation for {recipient_club} — BoilerMake XIII"

    # Attach body text (customizable)
    msg.attach(MIMEText(EMAIL_BODY, "plain"))

    # -----------------------------------------
    # Attach PNG flyer
    # -----------------------------------------
    with open(ATTACHMENT_PATH, "rb") as attachment:
        mime = MIMEBase("application", "octet-stream")
        mime.set_payload(attachment.read())
        encoders.encode_base64(mime)
        mime.add_header(
            "Content-Disposition",
            f"attachment; filename={ATTACHMENT_PATH}",
        )
        msg.attach(mime)

    # -----------------------------------------
    # Setup secure Gmail connection
    # -----------------------------------------
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(GMAIL_ADDRESS, APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, recipient_email, msg.as_string())

    print(f"✔ Sent to {recipient_club} ({recipient_email} at {recipient_university})")

# -----------------------------------------
# 5. LOOP THROUGH CSV AND SEND
# -----------------------------------------
def main():
    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            university = row["university"]
            club = row["club"]
            email = row["contact_email"]

            try:
                send_email(university, email, club)
            except Exception as e:
                print(f"❌ Failed for {club} ({email}): {e}")

if __name__ == "__main__":
    print("🚀 Sending emails...")
    main()
    print("✨ All emails processed.")