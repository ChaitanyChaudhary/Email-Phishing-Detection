import imaplib
import logging
import config
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('email_checker.log', maxBytes=2000, backupCount=5)
logging.basicConfig(handlers=[handler], level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def login_to_gmail():
    try:
        # Connect to the Gmail IMAP server
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        logging.info("Connected to Gmail IMAP server.")

        # Log in using credentials from config.py
        mail.login(config.EMAIL, config.PASSWORD)
        logging.info("Logged in successfully!")

        return mail
    except imaplib.IMAP4.error as e:
        logging.error(f"IMAP error occurred during login: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred during login: {e}")
    return None

if __name__ == "__main__":
    mail = login_to_gmail()
    if mail:
        print("Login successful.")
    else:
        print("Login failed. Check the logs for more details.")

