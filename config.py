import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
