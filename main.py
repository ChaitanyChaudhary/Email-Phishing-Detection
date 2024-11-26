import psutil
import time
import sys
import logging
from login import login_to_gmail
from capture_email import fetch_emails
from spamDetector import check_email_for_spam
from phishingDetector import train_phishing_detector, check_email_for_phishing
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('email_checker.log', maxBytes=2000, backupCount=5)
logging.basicConfig(handlers=[handler], level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Train or load phishing detection model and vectorizer
    try:
        model, vectorizer = train_phishing_detector()
        logging.info("Phishing detection model and vectorizer loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to train or load phishing detection model: {e}")
        sys.exit("Exiting due to model loading error.")

    mail = login_to_gmail()
    if mail:
        try:
            while True:
                email_contents = fetch_emails(mail, num_emails=10)  # Fetch multiple emails
                if email_contents:
                    for email_content in email_contents:  # Iterate over each email content
                        try:
                            if not check_email_for_spam(email_content):
                                # If not spam, check for phishing
                                check_email_for_phishing(email_content, model, vectorizer)
                        except Exception as e:
                            logging.error(f"Error processing email: {e}")

                # Monitor resource usage
                cpu_usage = psutil.cpu_percent(interval=1)
                memory_info = psutil.virtual_memory()
                logging.info(f"CPU Usage: {cpu_usage}%")
                logging.info(f"Memory Usage: {memory_info.percent}%")

                # Adjust sleep interval based on resource usage
                sleep_interval = 120 if cpu_usage > 80 or memory_info.percent > 80 else 60
                logging.info(f"Sleeping for {sleep_interval} seconds.")
                time.sleep(sleep_interval)
        except KeyboardInterrupt:
            logging.info("Program interrupted by user. Exiting...")
            sys.exit("Program interrupted. Exiting...")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            sys.exit("Exiting due to unexpected error.")
    else:
        logging.error("Failed to log in to Gmail. Exiting...")
        sys.exit("Exiting due to login failure.")

if __name__ == "__main__":
    main()
