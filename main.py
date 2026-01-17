import os
import logging
import re
import pickle
import time
import pandas as pd
import imaplib
import email
from logging.handlers import RotatingFileHandler
from login import login_to_gmail
from phishingDetector import (
    load_model_and_vectorizer,
)

# Set up logging
handler = RotatingFileHandler('email_checker.log', maxBytes=2000, backupCount=5)
logging.basicConfig(handlers=[handler], level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_unread_emails(mail):
    """Fetches unread emails from the Gmail inbox."""
    try:
        mail.select("inbox")
        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()
        logging.info(f"Fetched {len(email_ids)} unread emails.")
        return email_ids
    except Exception as e:
        logging.error(f"Error fetching unread emails: {e}")
        raise

def process_email(mail, email_id):
    """Processes an email and returns its subject, sender, and body."""
    try:
        status, data = mail.fetch(email_id, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Extract email components
        subject = msg["Subject"] or ""
        sender = msg["From"] or ""
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        logging.info(f"Email parsed: Subject: {subject}, Sender: {sender}")
        return subject, sender, body

    except Exception as e:
        logging.error(f"Error processing email: {e}")
        raise

def main():
    # Log in to Gmail using login.py
    mail = login_to_gmail()
    if not mail:
        logging.error("Failed to log in to Gmail. Exiting.")
        return

    # Load model and vectorizer
    try:
        with open('phishing_model.pkl', 'rb') as model_file:
            model = pickle.load(model_file)
        with open('vectorizer.pkl', 'rb') as vectorizer_file:
            vectorizer = pickle.load(vectorizer_file)
        logging.info("Model and vectorizer loaded successfully.")
    except Exception as e:
        logging.error(f"Error loading model or vectorizer: {e}")
        raise

    while True:
        try:
            # Fetch unread emails
            email_ids = fetch_unread_emails(mail)

            for email_id in email_ids:
                subject, sender, body = process_email(mail, email_id)

                # Transform the email body into the feature space
                body_vector = vectorizer.transform([body])
                body_vector_dense = body_vector.toarray().reshape(1, -1)

                # Get prediction
                prediction = model.predict(body_vector_dense)[0]
                prediction_label = "Legitimate" if prediction == 1 else "Phishing"
                logging.info(f"This email is classified as {prediction} - {prediction_label}: {subject}")
                print(f"This email is classified as {prediction} ({prediction_label}) - {subject}")

            # Wait 60 seconds before checking again
            time.sleep(60)

        except Exception as e:
            logging.error(f"Error during email checking loop: {e}")

if __name__ == "__main__":
    main()
