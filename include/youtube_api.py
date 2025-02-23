import logging
import googleapiclient.discovery

from include.utils import load_api_key, save_to_json, save_to_csv
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    """
    Extracts the transcript of a given youtube video
    
    Args:
        video_id (str): ID of a YouTube Video

    Returns:
        str: Transcript of a Video
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        logging.debug(f"get_transcript() - Successfully retrieved Transcript for ID {video_id}")

        return " ".join([entry["text"] for entry in transcript])
    except Exception as e:
        logging.error("An Error occured while getting the Transcript", exc_info=True)

        return None

def get_youtube_service():
    api_key = load_api_key()
    logging.debug("get_youtube_service() - Created the Google API object")

    return googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

def search_videos(query, max_results=1000):
    """
    Queries YouTube using its API to find
    n number of videos resulting from a given query

    Args:
        query (str): String query to pass to YouTube's API
        max_results (int): Number of Videos to return

    Returns:
        List: Results from a query in a List format
    """
    youtube = get_youtube_service()
    request = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=max_results,
        type="video"
    )
    response = request.execute()
    logging.debug("search_videos() - Got the list of videos")

    return response.get("items", [])

def get_video_details(video_id):
    youtube = get_youtube_service()
    request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    )
    response = request.execute()
    logging.debug(f"get_video_details() - Got the details for ID {video_id}")

    return response.get("items", [])[0]

def get_video_comments(video_id, max_results=100):
    """
    Gets an n number of comments left under a given YouTube Video

    Args:
        video_id (str): ID of a YouTube Video
        max_results (int): Number of comments to retrieve

    Returns:
        List: Comments under a Video in a List format
    """
    try:
        youtube = get_youtube_service()
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            textFormat="plainText"
        )
        response = request.execute()
        logging.debug(f"get_video_comments() - Got {max_results} for ID {video_id}")

        return response.get("items", [])
    except Exception as e:
        return []

def fetch_video_data(query):
    """Main Entry"""
    videos = search_videos(query)
    results = []

    for video in videos:
        video_id = video["id"]["videoId"]
        details = get_video_details(video_id)
        transcript = get_transcript(video_id)
        comments = get_video_comments(video_id)

        try:
            if comments != []:
                video_data = {
                    "video_id": video_id,
                    "title": details["snippet"]["title"],
                    "views": details["statistics"]["viewCount"],
                    "likes": details["statistics"]["likeCount"],
                    "transcript": transcript,
                    "comments": [
                        {
                            "text": comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                            "likes": comment["snippet"]["topLevelComment"]["snippet"]["likeCount"]
                        }
                        for comment in comments
                    ]
                }
            else:
                video_data = {
                    "video_id": video_id,
                    "title": details["snippet"]["title"],
                    "views": details["statistics"]["viewCount"],
                    "likes": details["statistics"]["likeCount"],
                    "transcript": transcript,
                }

            results.append(video_data)
        except KeyError as e:
            logging.warning("Like Count is Hidden", exc_info=True)
            continue

    save_to_json(results, f"{query}_data.json")

    for result in results:
        save_to_csv(result, f"{query}_data.csv")
