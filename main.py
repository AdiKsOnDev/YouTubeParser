import logging

from include.youtube_api import get_transcript, search_videos, get_video_details, get_video_comments, fetch_video_data
from include.utils import save_to_json

class RootOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.name == "root"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.addFilter(RootOnlyFilter())
logger.addHandler(ch)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    query = input("Enter your search query: ")
    fetch_video_data(query)
