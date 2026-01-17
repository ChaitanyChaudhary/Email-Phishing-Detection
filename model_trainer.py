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

def preprocess_text(text):
    """
    Preprocess email text content.
    """
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(text.lower())
    filtered_words = [w for w in words if w.isalpha() and w not in stop_words]
    return " ".join(filtered_words)

def train_model(csv_path):
    """
    Train a phishing detection model using a CSV dataset.
    Returns the trained model and vectorizer.
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

def load_model():
    """
    Load the trained model and vectorizer from disk.
    Returns the model and vectorizer.
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

def get_or_train_model(csv_path='emails.csv'):
    """
    Get the existing model or train a new one if not available.
    Returns the model and vectorizer.
    """
    if os.path.exists('phishing_model.pkl') and os.path.exists('vectorizer.pkl'):
        logging.info("Loading existing model and vectorizer...")
        return load_model()
    else:
        logging.info("Training new model from dataset...")
        return train_model(csv_path)

if __name__ == '__main__':
    # Example usage
    model, vectorizer = get_or_train_model() 