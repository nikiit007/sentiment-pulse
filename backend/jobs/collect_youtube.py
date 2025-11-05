import os
import json
from datetime import datetime
from backend.adapters.youtube import YouTubeAPI
from backend.models.config import settings

def run_once():
    if settings.DEMO_MODE and not settings.YOUTUBE_API_KEY:
        print("DEMO_MODE: Loading from seed file.")
        today = datetime.now().strftime("%Y-%m-%d")
        raw_dir = f"data/raw/{today}"
        os.makedirs(raw_dir, exist_ok=True)
        output_path = f"{raw_dir}/youtube.ndjson"
        with open("data/seeds/youtube_demo.ndjson", "r") as f_in, open(output_path, "w") as f_out:
            f_out.write(f_in.read())
        print(f"Wrote seed data to {output_path}")
        return {"status": "success", "counts": {"videos_scanned": 0, "comments_written": 10}, "path": output_path}

    if not settings.YOUTUBE_API_KEY:
        print("YOUTUBE_API_KEY not found in .env file.")
        return {"status": "error", "message": "YOUTUBE_API_KEY not found."}

    youtube = YouTubeAPI(settings.YOUTUBE_API_KEY)

    # Load show config if it exists
    try:
        with open("data/ShowConfig.json", "r") as f:
            show_config = json.load(f)
            search_terms = show_config.get("youtube_search_terms", settings.YT_SEARCH_TERMS)
    except FileNotFoundError:
        search_terms = settings.YT_SEARCH_TERMS

    videos = youtube.search_videos(search_terms, settings.YT_PUBLISHED_AFTER, settings.YT_MAX_VIDEOS)
    
    today = datetime.now().strftime("%Y-%m-%d")
    raw_dir = f"data/raw/{today}"
    os.makedirs(raw_dir, exist_ok=True)
    output_path = f"{raw_dir}/youtube.ndjson"

    comments_written = 0
    with open(output_path, "w", encoding="utf-8") as f:
        for video in videos:
            comments = youtube.fetch_comment_threads(video["videoId"], settings.YT_MAX_COMMENTS_PER_VIDEO)
            for comment in comments:
                mention = {
                    "platform": "youtube",
                    "external_id": comment["id"],
                    "created_at": comment["publishedAt"],
                    "author": comment["authorDisplayName"],
                    "text": comment["text"],
                    "lang": "en",
                    "meta": {
                        "video_id": video["videoId"],
                        "video_title": video["title"],
                        "channel_id": video["channelId"],
                        "like_count": comment["likeCount"]
                    },
                    "entities": {"characters": [], "hashtags": [], "keywords": []},
                    "sentiment": {"label": None, "score": None},
                    "topics": [],
                    "show_id": "your_show", # Replace with actual show_id
                    "episode_id": None
                }
                f.write(json.dumps(mention) + "\n")
                comments_written += 1

    print(f"Videos scanned: {len(videos)}")
    print(f"Comments written: {comments_written}")
    print(f"Output written to {output_path}")
    return {"status": "success", "counts": {"videos_scanned": len(videos), "comments_written": comments_written}, "path": output_path}

if __name__ == "__main__":
    run_once()
