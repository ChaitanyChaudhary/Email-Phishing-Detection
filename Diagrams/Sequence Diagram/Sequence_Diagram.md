# Email Phishing Detection – Sequence Diagram

## Participants

* **User**
* **Main**
* **Config**
* **Logging**
* **Login**
* **Gmail**
* **ModelTrainer**
* **PhishingDetector**
* **MLModel**
* **Vectorizer**

---

## Sequence of Interactions

### 1. Application Startup

1. **User → Main**
   Start application.

2. **Main → Config**
   Load environment variables.
   **Config → Main**: Return configuration data.

3. **Main → Logging**
   Initialize logging system.
   **Logging → Main**: Logging system ready.

---

### 2. Gmail Authentication

4. **Main → Login**
   Authenticate with Gmail.

5. **Login → Gmail**
   Connect to IMAP server.
   **Gmail → Login**: Connection established.

6. **Login → Gmail**
   Login using credentials.
   **Gmail → Login**: Authentication result.

---

## Authentication Decision

### If Authentication Is Successful

7. **Login → Main**
   Return mail connection.

---

## 3. Model Management

8. **Main → ModelTrainer**
   Check for existing model.
   **ModelTrainer → Main**: Model check result.

### If Model Exists

9. **Main → ModelTrainer**
   Load model and vectorizer.

10. **ModelTrainer → MLModel**
    Load model from file.
    **MLModel → ModelTrainer**: Model loaded.

11. **ModelTrainer → Vectorizer**
    Load vectorizer from file.
    **Vectorizer → ModelTrainer**: Vectorizer loaded.

12. **ModelTrainer → Main**
    Model and vectorizer ready.

---

### If No Model Exists

13. **Main → ModelTrainer**
    Train new model.

14. **ModelTrainer → ModelTrainer**
    Load training dataset (`emails.csv`).

15. **ModelTrainer → ModelTrainer**
    Preprocess text data (clean and normalize).

16. **ModelTrainer → Vectorizer**
    Fit TF-IDF vectorizer.
    **Vectorizer → ModelTrainer**: Vectorizer trained.

17. **ModelTrainer → MLModel**
    Train Naive Bayes model.
    **MLModel → ModelTrainer**: Model trained.

18. **ModelTrainer → ModelTrainer**
    Save model and vectorizer to files.

19. **ModelTrainer → Main**
    Training complete.

---

## 4. Email Monitoring Loop (Continuous)

20. **Main → Gmail**
    Fetch unread emails.
    **Gmail → Main**: Return email list.

---

### For Each Email

21. **Main → PhishingDetector**
    Process email.

22. **PhishingDetector → PhishingDetector**
    Parse email components and extract raw data.

23. **PhishingDetector → PhishingDetector**
    Extract subject and body from headers.

24. **PhishingDetector → PhishingDetector**
    Preprocess and clean email text.

25. **PhishingDetector → Vectorizer**
    Transform text into feature vector.
    **Vectorizer → PhishingDetector**: Feature vector returned.

26. **PhishingDetector → MLModel**
    Predict classification.
    **MLModel → PhishingDetector**: Prediction result.

27. **PhishingDetector → Logging**
    Log analysis result.
    **Logging → PhishingDetector**: Log entry created.

28. **PhishingDetector → Main**
    Return classification result.

29. **Main → User**
    Display classification result.

---

30. **Main → Main**
    Wait 60 seconds (sleep).

31. **Main → Main**
    Continue email monitoring loop.

---

## If Authentication Fails

7. **Login → Main**
   Authentication failed.

8. **Main → Logging**
   Log error.
   **Logging → Main**: Error logged.

9. **Main → User**
   Display error and exit application.

---

## Sequence Summary

### Phase 1: Initialization

* Application startup
* Configuration loading
* Logging initialization
* Gmail authentication

### Phase 2: Model Management

* Check for existing model
* Load model if available
* Train model if not available
* Prepare model and vectorizer

### Phase 3: Email Processing Loop

* Fetch unread emails
* Process each email
* Predict phishing or legitimate
* Log and display results
* Repeat every 60 seconds

### Phase 4: Error Handling

* Authentication failures terminate application
* Processing errors are logged
* Model loading errors raise exceptions

---

## Data Flow

**Input**

* Configuration data
* Gmail emails via IMAP
* Training dataset (CSV)

**Processing**

* Text preprocessing
* Feature extraction (TF-IDF)
* Classification (Naive Bayes)

**Output**

* Results displayed to user
* Logs written to files
* Trained models saved to disk

---