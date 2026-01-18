# Email Phishing Detection – Flow Diagram

## 1. Application Initialization

1. **Start Application**
2. **Load Configuration**

   * Load environment variables and settings from the configuration file.
3. **Initialize Logging System**

   * Set up rotating log file handlers for system logging.
4. **Gmail Authentication**

   * Connect to the Gmail IMAP server using credentials.

### Decision: Is Login Successful?

* **No**

  * Log error and exit the application.
* **Yes**

  * Proceed to model loading.

---

## 2. Model Management Phase

### Load Machine Learning Model and Vectorizer

* Check whether model files exist on disk.

#### Decision: Do Model Files Exist?

* **No – Train New Model**

  1. Load training dataset (`emails.csv`) with labeled data.
  2. Preprocess email text

     * Clean and normalize content
     * Remove stop words and tokenize.
  3. TF-IDF Vectorization

     * Convert text into numerical features.
  4. Train Naive Bayes machine learning model.
  5. Save trained model and vectorizer

     * `phishing_model.pkl`
     * `vectorizer.pkl`
  6. Proceed to email monitoring loop.

* **Yes – Load Existing Model**

  * Load the saved model and vectorizer from disk.
  * Proceed to email monitoring loop.

---

## 3. Email Monitoring Loop (Continuous)

1. **Fetch Unread Emails from Gmail**

   * Query the Gmail inbox for unread emails via IMAP.

### Decision: Are New Emails Found?

* **No**

  * Wait 60 seconds.
  * Return to the start of the email monitoring loop.

* **Yes – Process Each Email Individually**

  1. Extract email components and metadata.
  2. Parse email subject, sender, and body content.

     * Handle both single-part and multipart emails.
  3. Preprocess and clean email text.

     * Normalize text
     * Remove special characters and stop words
     * Tokenize and filter words.
  4. Extract TF-IDF features from text.
  5. Perform machine learning model prediction.

     * Obtain prediction probabilities.

---

## 4. Phishing Detection Decision

### Decision: Is a Phishing Attack Detected?

* **Yes**

  * Log phishing alert and warning.
  * Display phishing warning to the user.
  * Continue monitoring for new emails.

* **No**

  * Log legitimate email confirmation.
  * Display legitimate email status to the user.
  * Continue monitoring for new emails.

---

## 5. Error Handling

* Authentication failures → Log error and exit.
* Email processing errors → Log error and continue execution.
* Model loading errors → Log error and raise exception.

---

## 6. Data Flow Summary

* **Input:** Gmail emails via IMAP protocol
* **Processing:** Text preprocessing and TF-IDF feature extraction
* **Analysis:** Machine learning classification
* **Output:** Phishing or legitimate email status
* **Storage:** Log files and persisted ML model files

---