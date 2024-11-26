import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from scipy.io import arff
import logging
from logging.handlers import RotatingFileHandler
import imaplib

# Configure logging
handler = RotatingFileHandler('email_checker.log', maxBytes=2000, backupCount=5)
logging.basicConfig(handlers=[handler], level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

nltk.download('punkt')
nltk.download('stopwords')

def load_datasets():
    try:
        # Load phishing data from ARFF file
        phishing_data, meta = arff.loadarff('Data/PhishingData.arff')
        phishing_df = pd.DataFrame(phishing_data)
        
        print("Columns in dataset:", phishing_df.columns)

        # Ensure the 'text' column is present
        if 'text' not in phishing_df.columns:
            raise ValueError("The 'text' column is missing from the phishing dataset.")

        # Convert byte strings to regular strings
        phishing_df['text'] = phishing_df['text'].apply(lambda x: x.decode('utf-8'))

        logging.info("Phishing data loaded successfully.")
        return phishing_df
    except Exception as e:
        logging.error(f"Error loading datasets: {e}")
        raise


def preprocess_text(text):
    try:
        tokens = word_tokenize(text)
        tokens = [word.lower() for word in tokens if word.isalpha()]
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words]
        return ' '.join(filtered_tokens)
    except Exception as e:
        logging.error(f"Error preprocessing text: {e}")
        return ""

def train_phishing_detector(data_path):
    try:
        # Load the dataset
        df = pd.read_csv(data_path)

        # Preprocess the text data (adjust as needed)
        df['text'] = df['text'].apply(lambda x: preprocess_text(x))

        # Create a TF-IDF vectorizer
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(df['text'])
        y = df['label']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create and train the model
        model = MultinomialNB()
        model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test)
        print(classification_report(y_test, y_pred))

        # Save the model and vectorizer
        joblib.dump(model, 'phishing_model.pkl')
        joblib.dump(vectorizer, 'vectorizer.pkl')

        return model, vectorizer

    except Exception as e:
        print(f"Error training phishing detector: {e}")
        return None, None

def load_model_and_vectorizer():
    try:
        model = joblib.load('phishing_model.pkl')
        vectorizer = joblib.load('vectorizer.pkl')
        logging.info("Model and vectorizer loaded successfully.")
        return model, vectorizer
    except Exception as e:
        logging.error(f"Error loading model and vectorizer: {e}")
        raise


def check_email_for_phishing(email_content, model, vectorizer):
    try:
        processed_email = preprocess_text(email_content)
        email_vector = vectorizer.transform([processed_email])
        prediction = model.predict(email_vector)
        if prediction[0] == 1:
            logging.info("This email is phishing.")
            print("This email is phishing.")
            # Action: Move to a phishing folder
            move_email_to_folder(email_content, 'Phishing')
        else:
            logging.info("This email is legitimate.")
            print("This email is legitimate.")
    except Exception as e:
        logging.error(f"Error checking email for phishing: {e}")

# Function to move email (implementation depends on your email server)
def move_email_to_folder(email_content, folder_name):
    try:
        # Establish an IMAP connection (example using Gmail)
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login('your_email@example.com', 'your_password')  # Use secure methods to handle credentials

        # Select the mailbox you want to move the email from
        mail.select('inbox')

        # Search for the email by some criteria (e.g., subject, date)
        result, data = mail.search(None, 'ALL')  # Adjust search criteria as needed
        email_ids = data[0].split()

        # Move the email to the specified folder
        for email_id in email_ids:
            mail.copy(email_id, folder_name)
            mail.store(email_id, '+FLAGS', '\\Deleted')

        mail.expunge()  # Permanently remove emails marked for deletion
        mail.logout()
        logging.info(f"Email moved to {folder_name} folder successfully.")
    except Exception as e:
        logging.error(f"Error moving email to folder: {e}")

if __name__ == "__main__":
    # Check if model and vectorizer exist, otherwise train
    if os.path.exists('phishing_model.pkl') and os.path.exists('vectorizer.pkl'):
        model, vectorizer = load_model_and_vectorizer()
    else:
        model, vectorizer = train_phishing_detector()

    # Example email content
    email_content = "Congratulations! You've won a prize. Click here to claim."
    check_email_for_phishing(email_content, model, vectorizer)
