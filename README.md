# Email Phishing Detection

This is an open-source project designed to detect spam and phishing emails using IMAP-based email fetching and machine learning. Contributions are welcome to improve its features and performance.

## Features

- **Phishing Detection**: Utilizes a trained machine learning model to identify phishing attempts with high accuracy.
- **Email Monitoring**: Periodically fetches emails from the Gmail inbox for real-time analysis.
- **Logging**: Includes rotating log files for debugging and monitoring.

## How It Works

1. **Email Fetching**: The system connects to a Gmail account using IMAP and fetches recent emails for processing.
2. **Phishing Detection**: Analyzes email content using a machine learning model trained on a phishing dataset.
3. **Insights**: Emails classified as phishing are logged and flagged for further action.

## Project Structure

- **main.py**: Orchestrates email fetching, phishing detection, and logging.
- **login.py**: Manages Gmail login using credentials stored securely in a .env file.
- **capture_email.py**: Handles email fetching from the inbox and phishing detection.
- **phishingDetector.py**: Contains the machine learning model and preprocessing pipeline for phishing detection.
- **model_trainer.py**: Handles model training and loading functionality.
- **config.py**: Loads email credentials and configuration from a .env file.
- **requirements.txt**: Lists all project dependencies.

## Setup

### Prerequisites
1. Ensure Python 3.7 or higher is installed.
2. Enable IMAP support in your Gmail account:
   - Log in to your Gmail account.
   - Go to **Settings** > **See all settings**.
   - Navigate to the **Forwarding and POP/IMAP** tab.
   - In the **IMAP access** section, select **Enable IMAP**.
   - Save changes.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ChaitanyChaudhary/Email-Phishing-Detection.git
   cd Email-Phishing-Detection
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Gmail credentials:
   ```
   EMAIL=your-email@gmail.com
   PASSWORD=your-email-password
   ```

4. Train the phishing detection model:
   - Place your labeled email dataset (e.g., `emails.csv`) in the project directory.
   - Run `phishingDetector.py` to train the model and save it locally.

5. Run the application:
   ```bash
   python main.py
   ```

## Logging

- Logs are saved to `email_checker.log` and rotate automatically when they reach 2 KB.
- Backup logs are stored with incremental numbering (e.g., `email_checker.log.1`, `email_checker.log.2`).

## Contributing

This project is open-source and licensed under the MIT License. Contributions are welcome, whether it’s fixing bugs, improving the codebase, or enhancing the model.

- Fork the repository.
- Create a new branch for your changes.
- Submit a pull request describing your contribution.

## Limitations

- **Email Provider**: Currently supports Gmail IMAP only. Other providers require IMAP server configuration updates in `login.py`.
- **Dataset**: A preprocessed phishing dataset is required to train the machine learning model.
- **Environment Variables**: Ensure a secure `.env` file for storing email credentials.

## License

This project is licensed under the [MIT](LICENSE) License.

## Authors

- [Chaitany Chaudhary](https://github.com/ChaitanyChaudhary)
