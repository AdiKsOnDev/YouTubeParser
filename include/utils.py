import json
import csv
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

def save_to_csv(data, filename):
    """
    Save a dictionary to a CSV file.

    Args:
        data (dict): The dictionary to save.
        filename (str): The name of the CSV file to save the dictionary to.
    """
    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", filename)

    with open(filepath, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        writer.writerow(data.keys())
        writer.writerow(data.values())

    print(f"Data saved to {filepath}")
