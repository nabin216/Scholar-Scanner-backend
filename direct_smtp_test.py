import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# AWS SES SMTP settings
smtp_host = "email-smtp.eu-north-1.amazonaws.com"  
smtp_port = 587
smtp_user = "AKIA2UCDHAJ7Y3XZHJHC"  
smtp_pass = "BEl+kWSS5N/iYKvei3COboT5KwlmKly1G8OGIs7c//04"
from_email = "asadurzamannabin@gmail.com"

print("AWS SES SMTP Direct Test")
print("-----------------------")
print(f"Host: {smtp_host}")
print(f"Port: {smtp_port}")
print(f"User: {smtp_user}")
print(f"From Email: {from_email}")

# Ask for recipient email
to_email = input("Enter recipient email address: ")

try:
    print("\nCreating email message...")
    msg = MIMEMultipart()
    msg['From'] = f'Scholarship Portal <{from_email}>'
    msg['To'] = to_email
    msg['Subject'] = 'AWS SES SMTP Test'
    msg.attach(MIMEText('This is a direct SMTP test from Scholarship Portal.', 'plain'))
    
    print("Connecting to SMTP server...")
    server = smtplib.SMTP(smtp_host, smtp_port)
    
    print("Starting TLS...")
    server.starttls()
    
    print("Authenticating...")
    server.login(smtp_user, smtp_pass)
    
    print("Sending email...")
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()
    
    print("\n✅ Email sent successfully!")
    print("Check your inbox (and spam folder) to confirm.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nPossible issues:")
    print("1. Invalid SMTP credentials")
    print("2. Email address not verified in AWS SES")
    print("3. AWS SES in sandbox mode (can only send to verified emails)")
    print("4. Network/firewall issues")
