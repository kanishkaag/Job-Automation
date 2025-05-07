from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

# Environment variables for security
EMAIL_ADDRESS = 'your_email@gmail.com'  # e.g., your Gmail address
EMAIL_PASSWORD = 'your_app_password' # your app password

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    to_email = data.get('to')
    subject = data.get('subject')
    body = data.get('body')

    if not all([to_email, subject, body]):
        return jsonify({'error': 'Missing fields'}), 400

    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg.set_content(body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        return jsonify({'message': 'Email sent successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
