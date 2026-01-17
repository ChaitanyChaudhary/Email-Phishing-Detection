'''
1 -> phishing.
0 -> legitimate.
'''

import email
import logging
from logging.handlers import RotatingFileHandler
from model_trainer import preprocess_text, get_or_train_model

# Configure logging
handler = RotatingFileHandler('email_checker.log', maxBytes=2000, backupCount=5)
logging.basicConfig(handlers=[handler], level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_email(raw_email):
    """
    Parse raw email and extract headers, subject, sender, and body.
    """
    msg = email.message_from_string(raw_email)
    subject = msg.get("Subject", "")
    sender = msg.get("From", "")
    headers = dict(msg.items())
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_payload(decode=True).decode(errors="ignore")
    else:
        body = msg.get_payload(decode=True).decode(errors="ignore")
    return subject, sender, headers, body

def check_email_for_phishing(subject, body, vectorizer, model):
    """
    Check if an email is phishing based on its features.
    """
    try:
        # Combine subject and body
        email_content = f"{subject} {body}"

        # Preprocess the combined content
        preprocessed_content = preprocess_text(email_content)

        # Convert the content to a feature vector
        content_vector = vectorizer.transform([preprocessed_content]).toarray()

        # Log feature vector
        logging.info(f"Feature vector (dense): {content_vector.shape}")

        # Get prediction probabilities (both phishing and legitimate probabilities)
        prediction_probabilities = model.predict_proba(content_vector)  # Returns probabilities for both classes
        logging.info(f"Prediction probabilities: {prediction_probabilities}")

        # If probabilities are low for phishing (class 1), it could be predicting wrongly
        phishing_prob = prediction_probabilities[0][1]  # Probability for phishing class (class 1)
        legitimate_prob = prediction_probabilities[0][0]  # Probability for legitimate class (class 0)
        logging.info(f"Phishing Probability: {phishing_prob}, Legitimate Probability: {legitimate_prob}")

        # Prediction label (the class)
        prediction = model.predict(content_vector)[0]  # Get final label (0 or 1)
        logging.info(f"Prediction label: {prediction}")

        # Output result
        if prediction == 1:
            print(f"This email is phishing - {subject}.")
        else:
            print(f"This email is legitimate - {subject}.")
    except Exception as e:
        logging.error(f"Error checking phishing status: {e}")
        raise

if __name__ == '__main__':
    try:
        # Get or train the model
        model, vectorizer = get_or_train_model()

        # Example email content (dynamic input can be added here)
        raw_email = """From: support@phishing.com
        Subject: Urgent! Verify Your Account
        
        Dear user,
        Please verify your account immediately to avoid suspension.
        Click here: http://phishing.com/verify
        """
        # Parse the email
        subject, sender, headers, body = parse_email(raw_email)
        logging.info(f"Email parsed: Subject: {subject}, Sender: {sender}")

        # Check if the email is phishing
        check_email_for_phishing(subject, body, vectorizer, model)
    except Exception as e:
        logging.error(f"An error occurred in the main script: {e}")
