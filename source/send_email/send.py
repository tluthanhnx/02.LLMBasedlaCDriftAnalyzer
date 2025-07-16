import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import markdown
# Thiết lập thông tin email

def send_email_to_member(result: str):
    result = markdown.markdown(result)
    message = Mail(
        from_email='nhphan.ai01@gmail.com',           # Địa chỉ email của bạn (phải được xác thực với SendGrid)
        to_emails='phannguyenhuu46@gmail.com',        # Người nhận
        subject='Detect Drift',
        html_content= result
    )
    
    sengrid_api_key = os.getenv('sengrid_api_key')
    try:
        # Gửi email
        sg = SendGridAPIClient(sengrid_api_key)  # Thay bằng API key của bạn
        response = sg.send(message)
        print(sengrid_api_key)
        print(f"Status Code: {response.status_code}")
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

