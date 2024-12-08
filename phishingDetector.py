'''
1 -> phishing.
0 -> legitimate.
'''

import os
import email
import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import nltk
from nltk.corpus import stopwords
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
handler = RotatingFileHandler('email_checker.log', maxBytes=2000, backupCount=5)
logging.basicConfig(handlers=[handler], level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Download NLTK data if needed
nltk.download('punkt')
nltk.download('stopwords')


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


def preprocess_text(text):
    """
    Preprocess email text content.
    """
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(text.lower())
    filtered_words = [w for w in words if w.isalpha() and w not in stop_words]
    return " ".join(filtered_words)


def train_spam_detector(csv_path):
    """
    Train a spam detection model using a CSV dataset.
    """
    try:
        # Load dataset from CSV
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Dataset file not found at {csv_path}")

        labeled_emails = pd.read_csv(csv_path)
        if 'body' not in labeled_emails.columns or 'label' not in labeled_emails.columns:
            raise ValueError("The dataset must have 'body' and 'label' columns.")

        # Combine subject and body into a single content field if subject is present
        if 'subject' in labeled_emails.columns:
            labeled_emails['content'] = labeled_emails.apply(
                lambda x: f"{x['subject']} {x['body']}" if pd.notnull(x['subject']) else x['body'], axis=1
            )
        else:
            labeled_emails['content'] = labeled_emails['body']

        # Preprocess the content
        labeled_emails['content'] = labeled_emails['content'].apply(preprocess_text)

        # Vectorize the content
        vectorizer = CountVectorizer(stop_words='english', max_features=1000)
        email_vectors = vectorizer.fit_transform(labeled_emails['content'])

        # Train a Naive Bayes model
        model = MultinomialNB(class_prior='balanced')
        model.fit(email_vectors, labeled_emails['label'])

        # Save the model and vectorizer
        with open('phishing_model.pkl', 'wb') as model_file:
            pickle.dump(model, model_file)
        with open('vectorizer.pkl', 'wb') as vectorizer_file:
            pickle.dump(vectorizer, vectorizer_file)

        logging.info("Model and vectorizer saved successfully.")
        return model, vectorizer
    except Exception as e:
        logging.error(f"Error during model training: {e}")
        raise


def load_model_and_vectorizer():
    """
    Load the trained model and vectorizer from disk.
    """
    try:
        with open('phishing_model.pkl', 'rb') as model_file:
            model = pickle.load(model_file)
        with open('vectorizer.pkl', 'rb') as vectorizer_file:
            vectorizer = pickle.load(vectorizer_file)
        logging.info("Model and vectorizer loaded successfully.")
        return model, vectorizer
    except Exception as e:
        logging.error(f"Error loading model or vectorizer: {e}")
        raise


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
        # Dataset CSV file path
        dataset_path = 'emails.csv'

        # Load the model or train a new one if not available
        if os.path.exists('phishing_model.pkl') and os.path.exists('vectorizer.pkl'):
            logging.info("Loading existing model and vectorizer...")
            model, vectorizer = load_model_and_vectorizer()
        else:
            logging.info("Training new model from dataset...")
            model, vectorizer = train_spam_detector(dataset_path)

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
