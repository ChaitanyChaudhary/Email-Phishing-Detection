import os
import re
import pandas as pd
from bs4 import BeautifulSoup  # For removing HTML tags

def clean_html(raw_html):
    """
    Remove HTML tags from raw text.
    """
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

def process_email_folder(input_folder, output_csv):
    """
    Process all email files in a folder, clean them, and save as a CSV.
    """
    emails = []
    for filename in os.listdir(input_folder):
        filepath = os.path.join(input_folder, filename)
        if os.path.isfile(filepath):
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                    raw_email = file.read()

                # Remove HTML tags
                cleaned_email = clean_html(raw_email)

                # Extract components (subject, from, and body)
                subject = re.search(r"Subject:(.*)", cleaned_email)
                sender = re.search(r"From:(.*)", cleaned_email)
                body_start = cleaned_email.find("\n\n")  # Body usually starts after the headers
                body = cleaned_email[body_start:].strip()

                # Store the cleaned data
                emails.append({
                    "subject": subject.group(1).strip() if subject else "",
                    "sender": sender.group(1).strip() if sender else "",
                    "body": body
                })
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

    # Convert to a DataFrame and save as CSV
    df = pd.DataFrame(emails)
    df["label"] = None  # Add a label column for future labeling
    df.to_csv(output_csv, index=False)
    print(f"Cleaned emails saved to {output_csv}")

if __name__ == "__main__":
    # Define the input folder and output CSV file
    input_folder = "Data/spam/"
    output_csv = "emails.csv"
    process_email_folder(input_folder, output_csv)
