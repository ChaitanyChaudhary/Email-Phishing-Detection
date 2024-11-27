# Email Phishing Detection

Email Phishing Detection is a Python project that monitors and analyzes incoming emails to identify phishing and spam attempts. Using machine learning and natural language processing, it classifies emails as phishing, spam, or legitimate while maintaining detailed logs and monitoring system resources.

This project is open-source, and I’m actively seeking contributors to help improve it. As a beginner in machine learning, I’ve made mistakes in the code, and some parts are a bit messy. Your guidance, bug fixes, or contributions would be greatly appreciated!
## Features

- Spam Detection: Detects emails with suspicious patterns using keyword-based matching and attachment analysis.
- Phishing Detection: Uses a trained machine learning model to identify phishing attempts with high accuracy.
- Email Monitoring: Periodically fetches emails from an inbox for real-time analysis.
- Logging: Includes rotating log files for easy debugging and monitoring.
- Resource Monitoring: Tracks CPU and memory usage to optimize performance.
- Attachment Analysis: Scans attachments for potentially malicious file types.


## How It Works

- Email Fetching: The system connects to a Gmail account using IMAP, fetches recent emails, and processes their contents.

- Spam Detection: Keywords in the email subject and body, as well as suspicious attachments, are analyzed to classify emails as spam.

- Phishing Detection: Non-spam emails are further analyzed using a trained machine learning model to detect phishing attempts.

- Actionable Insights: Emails classified as phishing or spam can be logged, flagged, or moved to specific folders for further investigation.

## Project Structure

The project is organized into several Python scripts, each handling specific tasks:

- main.py: The main entry point of the application, orchestrating email fetching, spam detection, phishing detection, and resource monitoring.

- login.py: Handles Gmail login via IMAP using credentials stored in environment variables.

- capture_email.py: Fetches emails from the Gmail inbox for processing.

- spamDetector.py: Implements spam detection based on keyword matching and attachment analysis.

- phishingDetector.py: Handles phishing detection using a trained machine learning model and vectorizer.

- config.py: Loads environment variables like email credentials from a .env file.

- requirements.txt: Lists all dependencies required for the project.

## Setup

1. Clone the repository:
```
git clone https://github.com/ChaitanyChaudhary/Email-Phishing-Detection.git
cd Email-Phishing-Detection
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Create a .env file with your email credentials:
```
EMAIL=your-email@gmail.com
PASSWORD=your-email-password
```

4. Prepare your phishing detection model:
- Place your dataset in the Data/ directory (e.g., PhishingData.arff).
Run phishingDetector.py to train the model and save it locally.

5. Run the application:
```
python main.py
```


## Logging

- Logs are saved to email_checker.log and rotate automatically when they reach 2 KB.

- Backup logs are stored with incremental numbering (e.g., email_checker.log.1).

## Current Challenges

This project is still a work in progress, and as a beginner in machine learning, I’ve encountered several challenges:
- Dataset Loading: Struggling to properly load and preprocess datasets.

- Model Training: Facing difficulties in training the ML model for phishing detection.

If you notice errors or inefficiencies in the code, please feel free to contribute or offer guidance. Even small fixes, advice, or suggestions would be a huge help!


## Contributing

This is an open-source project licensed under the MIT License. Contributions are welcome, whether it’s fixing bugs, reviewing the code, or helping improve the model.

Here’s the [GitHub Repository](https://github.com/ChaitanyChaudhary/Email-Phishing-Detection). Please check it out and feel free to submit pull requests or issues.


## Limitations

- Email Service: Currently supports Gmail IMAP. For other email providers, update the IMAP server configuration in login.py.

- Dataset: Dataset: A preprocessed phishing dataset is required to train the model.

- Environment: Requires a .env file for securely storing email credentials.

## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License.


## Authors

- [Chaitany Chaudhary](https://github.com/ChaitanyChaudhary)
