import logging
import imaplib
from email import message_from_bytes
from phishingDetector import load_model_and_vectorizer, preprocess_text
from spamDetector import extract_subject, extract_body, is_spam
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

        email_contents = []
        for email_id in email_ids[-num_emails:]:
            result, message_data = mail.fetch(email_id, '(RFC822)')
            if result != 'OK':
                logging.error(f"Failed to fetch email ID {email_id}.")
                continue

            # Parse email content into a readable format
            raw_email = message_data[0][1]
            email_message = message_from_bytes(raw_email)
            email_contents.append(email_message)
            logging.info(f"Email ID {email_id} fetched successfully!")

        return email_contents
    except imaplib.IMAP4.error as e:
        logging.error(f"IMAP error occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    return []

# Load the spam detection model and vectorizer
model, vectorizer = load_model_and_vectorizer()

def check_email_for_spam(email_content):
    try:
        # Extract subject and body
        subject = extract_subject(email_content)
        body = extract_body(email_content)

        # Preprocess the email text
        combined_text = preprocess_text(subject + " " + body)

        # Transform text into TF-IDF features
        email_features = vectorizer.transform([combined_text])

        # Predict using the trained model
        prediction = model.predict(email_features)[0]
        if prediction == 1:
            logging.info(f"Spam detected in email with subject: {subject}")
            print(f"Spam detected: {subject}")
        else:
            logging.info(f"Email with subject: {subject} is not spam.")
            print(f"Not spam: {subject}")
    except Exception as e:
        logging.error(f"Error during spam detection: {e}")

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
