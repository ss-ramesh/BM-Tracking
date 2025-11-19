import smtplib
import ssl
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

GMAIL_ADDRESS = "santosh@boilermake.org"
APP_PASSWORD = "your_16_digit_app_password"  # DO NOT use your real Gmail password

CSV_PATH = "Outside Clubs _ Orgs - Sheet1 (1).csv"
EMAIL_DRAFT_PATH = "email-draft.txt"
ATTACHMENT_PATH = "Apps open flyer (1).png"

with open(EMAIL_DRAFT_PATH, "r") as f: 
    EMAIL_BODY = f.read()

def send_email(recipient_university, recipient_email, recipient_club):
    msg = MIMEMultipart()
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = recipient_email
    msg["Subject"] = f"Invitation for {recipient_club} — BoilerMake XIII"

    # Attach email body
    msg.attach(MIMEText(EMAIL_BODY, "plain"))

    # Attach flyer
    with open(ATTACHMENT_PATH, "rb") as attachment:
        mime = MIMEBase("application", "octet-stream")
        mime.set_payload(attachment.read())
        encoders.encode_base64(mime)
        mime.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(ATTACHMENT_PATH)}",
        )
        msg.attach(mime)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(GMAIL_ADDRESS, APP_PASSWORD)

        try:
            server.sendmail(GMAIL_ADDRESS, recipient_email, msg.as_string())
        except Exception as send_err:
            print(f"❌ Error sending to {recipient_email}: {send_err}")
            return

    print(f"✔ Sent to {recipient_club} ({recipient_email}, {recipient_university})")

def main():
    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not (row["Email"]) and row["Club / Org Name"]:
                continue
            university = row["University"]
            club = row["Club / Org Name"]
            email = row["Email"]
            try:
                send_email(university, email, club)
            except Exception as e:
                print(f"❌ Failed for {club} ({email}): {e}")

if __name__ == "__main__":
    print("🚀 Sending emails...")
    main()
    print("✨ All emails processed.")