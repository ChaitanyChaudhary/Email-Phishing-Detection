import logging
import imaplib
from spamDetector import is_spam
from login import login_to_gmail
import time
from logging.handlers import RotatingFileHandler

# Use logging.handlers for rotating logs
handler = RotatingFileHandler('email_checker.log', maxBytes=2000, backupCount=5)
logging.basicConfig(handlers=[handler], level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_emails(mail, num_emails=10):
    try:
        mail.select('inbox')
        result, data = mail.search(None, 'ALL')

        if result != 'OK':
            logging.error("Failed to search emails.")
            return []

        email_ids = data[0].split()
        if not email_ids:
            logging.info("No emails found.")
            return []

        # Fetch the last `num_emails` emails
        email_contents = []
        for email_id in email_ids[-num_emails:]:
            result, message_data = mail.fetch(email_id, '(RFC822)')
            if result != 'OK':
                logging.error(f"Failed to fetch email ID {email_id}.")
                continue

            raw_email = message_data[0][1]
            email_contents.append(raw_email)
            logging.info(f"Email ID {email_id} fetched successfully!")

        return email_contents
    except imaplib.IMAP4.error as e:
        logging.error(f"IMAP error occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    return []

def check_email_for_spam(email_content):
    try:
        if is_spam(email_content):
            logging.info("This email is spam.")
        else:
            logging.info("This email is not spam.")
    except Exception as e:
        logging.error(f"Error checking email for spam: {e}")

def main():
    mail = login_to_gmail()
    if mail:
        while True:
            email_contents = fetch_emails(mail, num_emails=10)
            if email_contents:
                for email_content in email_contents:
                    check_email_for_spam(email_content)
            else:
                logging.info("Waiting for new emails...")
            time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    main()
