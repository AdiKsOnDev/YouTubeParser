from include.youtube_api import get_transcript, search_videos, get_video_details, get_video_comments, fetch_video_data
from include.utils import save_to_json

if __name__ == "__main__":
    query = input("Enter your search query: ")
    fetch_video_data(query)
