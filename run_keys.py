import os
from dotenv import load_dotenv

load_dotenv()

def set_keys():
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key
        print("OPENAI_API_KEY has been set successfully.")
    else:
        print("OPENAI_API_KEY is not set. Please check your .env file.")