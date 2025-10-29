
import requests
import time
from typing import List, Dict, Optional

class YouTubeAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"

    def search_videos(self, search_terms: List[str], published_after: str, max_videos: int) -> List[Dict]:
        videos = []
        next_page_token = None
        while len(videos) < max_videos:
            params = {
                "part": "snippet",
                "q": " ".join(search_terms),
                "type": "video",
                "order": "date",
                "publishedAfter": published_after,
                "maxResults": min(50, max_videos - len(videos)),
                "key": self.api_key,
                "pageToken": next_page_token
            }
            try:
                response = requests.get(f"{self.base_url}/search", params=params)
                response.raise_for_status()
                data = response.json()
                for item in data.get("items", []):
                    videos.append({
                        "videoId": item["id"]["videoId"],
                        "title": item["snippet"]["title"],
                        "channelId": item["snippet"]["channelId"],
                        "publishedAt": item["snippet"]["publishedAt"]
                    })
                next_page_token = data.get("nextPageToken")
                if not next_page_token:
                    break
            except requests.exceptions.RequestException as e:
                print(f"Error searching videos: {e}")
                break
        return videos

    def fetch_comment_threads(self, video_id: str, max_comments: int) -> List[Dict]:
        comments = []
        next_page_token = None
        while len(comments) < max_comments:
            params = {
                "part": "snippet,replies",
                "videoId": video_id,
                "order": "time",
                "textFormat": "plainText",
                "maxResults": min(100, max_comments - len(comments)),
                "key": self.api_key,
                "pageToken": next_page_token
            }
            try:
                response = requests.get(f"{self.base_url}/commentThreads", params=params)
                if response.status_code == 403:
                    # Comments are disabled for this video
                    return []
                response.raise_for_status()
                data = response.json()
                for item in data.get("items", []):
                    top_level_comment = item["snippet"]["topLevelComment"]["snippet"]
                    comments.append({
                        "id": item["snippet"]["topLevelComment"]["id"],
                        "text": top_level_comment["textDisplay"],
                        "authorDisplayName": top_level_comment.get("authorDisplayName"),
                        "likeCount": top_level_comment["likeCount"],
                        "publishedAt": top_level_comment["publishedAt"]
                    })
                    if "replies" in item:
                        for reply in item["replies"]["comments"]:
                            reply_snippet = reply["snippet"]
                            comments.append({
                                "id": reply["id"],
                                "text": reply_snippet["textDisplay"],
                                "authorDisplayName": reply_snippet.get("authorDisplayName"),
                                "likeCount": reply_snippet["likeCount"],
                                "publishedAt": reply_snippet["publishedAt"]
                            })
                next_page_token = data.get("nextPageToken")
                if not next_page_token:
                    break
            except requests.exceptions.RequestException as e:
                print(f"Error fetching comments for video {video_id}: {e}")
                # Implement naive sleep/backoff
                if response.status_code in [429, 500, 502, 503, 504]:
                    time.sleep(5)
                else:
                    break
        return comments
