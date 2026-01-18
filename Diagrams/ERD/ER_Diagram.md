## EPD - EMAIL PHISHING DETECTION

### ENTITY–RELATIONSHIP DIAGRAM (Simple Text Format)

---

## ENTITIES

---

### 1. USERS

* user_id (Primary Key)
* email
* password

---

### 2. EMAILS

* email_id (Primary Key)
* user_id (Foreign Key → USERS)
* subject
* sender
* body
* headers
* received_date
* is_multipart
* content_type

---

### 3. ML_MODELS

* model_id (Primary Key)
* model_name
* model_type
* training_date
* accuracy_score

---

### 4. MODEL_VERSIONS

* version_id (Primary Key)
* model_id (Foreign Key → ML_MODELS)
* version_name
* created_at

---

### 5. PHISHING_ANALYSES

* analysis_id (Primary Key)
* email_id (Foreign Key → EMAILS)
* version_id (Foreign Key → MODEL_VERSIONS)
* phishing_probability
* confidence_score

---

### 6. TRAINING_DATA

* data_id (Primary Key)
* label
* source

---

### 7. MODEL_TRAINING (Junction Table)

* model_id (Foreign Key → ML_MODELS)
* data_id (Foreign Key → TRAINING_DATA)
* Composite Primary Key: (model_id, data_id)

---

### 8. LOG_RECORDS

* log_id (Primary Key)
* user_id (Foreign Key → USERS)
* action_type
* timestamp

---

## RELATIONSHIPS

---

1. **USERS → EMAILS**

   * One-to-Many
   * One user can receive many emails

2. **USERS → LOG_RECORDS**

   * One-to-Many
   * One user can generate many log records

3. **EMAILS → PHISHING_ANALYSES**

   * One-to-Many
   * One email can have multiple analysis results

4. **ML_MODELS → MODEL_VERSIONS**

   * One-to-Many
   * One model can have multiple versions

5. **MODEL_VERSIONS → PHISHING_ANALYSES**

   * One-to-Many
   * One model version can be used for many analyses

6. **ML_MODELS ↔ TRAINING_DATA**

   * Many-to-Many
   * Implemented via MODEL_TRAINING junction table

---

## SUMMARY

* Total Entities: **8**
* Normal Form: **3NF**

---