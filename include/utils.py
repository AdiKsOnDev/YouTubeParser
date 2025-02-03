import json
import os
from dotenv import load_dotenv

load_dotenv()

def load_api_key():
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("YouTube API key not found in .env file.")

    return api_key

def save_to_json(data, filename):
    """
    Saves given data in a JSON format

    Args:
        data (dict): Data to be saved
        filename (str): Name of the output file
    """
    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"Data saved to {filepath}")
