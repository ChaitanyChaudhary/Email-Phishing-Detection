import logging
import re
from email import message_from_bytes
import psutil
from phishingDetector import check_email_for_phishing
from logging.handlers import RotatingFileHandler
from bs4 import BeautifulSoup

handler = RotatingFileHandler('email_checker.log', maxBytes=2000, backupCount=5)
logging.basicConfig(handlers=[handler], level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def remove_html_tags(text):
    try:
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()
    except Exception as e:
        logging.error(f"An error occurred while removing HTML tags: {e}")
        return text


def extract_subject(email_message):
    return email_message['subject'] if email_message['subject'] else ""


def extract_body(email_message):
    body = ""
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() in ["text/plain", "text/html"]:
                payload = part.get_payload(decode=True)
                if payload:
                    body = payload.decode('utf-8', errors='ignore')
                    body = remove_html_tags(body)
                break
    else:
        payload = email_message.get_payload(decode=True)
        if payload:
            body = payload.decode('utf-8', errors='ignore')
            body = remove_html_tags(body)
    return body


def extract_attachments(email_message):
    attachments = []
    for part in email_message.walk():
        if part.get_content_disposition() == 'attachment':
            filename = part.get_filename()
            payload = part.get_payload(decode=True)
            attachments.append((filename, payload))
    return attachments


def analyze_attachment(filename, payload):
    # Placeholder for analysis logic
    if filename.endswith(('.exe', '.bat', '.cmd')):
        return True  # Considered suspicious
    # Add more checks as needed
    return False


def is_spam(email_content):
    try:
        email_message = message_from_bytes(email_content)
        subject = extract_subject(email_message)
        body = extract_body(email_message)

        spam_indicators = [
            "account suspended", "verify your account", "click here", "winner", "limited time offer",
            "act now", "congratulations", "you have been selected", "risk-free", "guaranteed", "you won the"
        ]

        indicator_count = sum(1 for indicator in spam_indicators if re.search(
            indicator, subject, re.IGNORECASE) or re.search(indicator, body, re.IGNORECASE))

        # Check attachments
        attachments = extract_attachments(email_message)
        for filename, payload in attachments:
            if analyze_attachment(filename, payload):
                logging.info(f"Suspicious attachment detected: {filename}")
                indicator_count += 1

        return indicator_count > 1

    except Exception as e:
        logging.error(f"An error occurred while checking for spam: {e}")
        return False


def check_email_for_spam(email_content):
    try:
        email_message = message_from_bytes(email_content)
        subject = extract_subject(email_message)
        if is_spam(email_content):
            logging.info(f"The email with subject '{subject}' is spam.")
            cpu_usage = psutil.cpu_percent(interval=1)
            logging.info(f"Current CPU usage: {cpu_usage}%")
        else:
            # Pass non-spam emails to phishing detection
            check_email_for_phishing(email_content)
    except Exception as e:
        logging.error(f"An error occurred while processing the email: {e}")


if __name__ == "__main__":
    # Example usage
    email_content = b"Subject: Congratulations! You have been selected to win a free prize.\n\nClick here to claim your prize now! Limited time offer!"
    check_email_for_spam(email_content)
