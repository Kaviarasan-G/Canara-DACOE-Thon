import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
def email_alert():
    port = 587
    smtp_server = "smtp.gmail.com"
    login = "canarabankmailalerts@gmail.com"  # Your Gmail email address
    password = "vxgs hzje lymc vlvi"  # Your Gmail App Password (generated in Gmail settings)

    sender_email = "canarabankmailalerts@gmail.com"
    receiver_email = "abamit17107@gmail.com"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Two Step Authentication Alert"
    message["From"] = sender_email
    message["To"] = receiver_email
    def generate_otp():
        return random.randint(100000, 999999)

    # Example usage
    OTP = generate_otp()    
    # Write the text/plain part
    text = f"""
    Dear [Customer Name],

    We have detected a potentially fraudulent transaction associated with your account. For your security, we have triggered a One-Time Password (OTP) to verify the authenticity of this transaction. Please use the following OTP within the next 10 minutes:

    OTP: {OTP}

    If you did not initiate this transaction or suspect any unauthorized activity, please contact our customer support immediately at [Customer Support Contact Details].

    Thank you for your cooperation in maintaining the security of your account.

    Best regards,
    Canara bank
    """
    # Write the HTML part


    # Convert both parts to MIMEText objects and add them to the MIMEMultipart message
    part1 = MIMEText(text, "plain")
    #part2 = MIMEText(html, "html")
    message.attach(part1)


    # Send your email using TLS (port 587)
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
email_alert()
