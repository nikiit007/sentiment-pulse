from pydantic import field_validator
from pydantic_settings import BaseSettings
from typing import List, Optional
from datetime import datetime, timedelta
import json

class YouTubeSettings(BaseSettings):
    YOUTUBE_API_KEY: Optional[str] = None
    YT_SEARCH_TERMS: List[str] = ["Your Show trailer", "Your Show review"]
    YT_PUBLISHED_AFTER: str = (datetime.now() - timedelta(days=7)).isoformat()
    YT_MAX_VIDEOS: int = 25
    YT_MAX_COMMENTS_PER_VIDEO: int = 200
    DEMO_MODE: bool = False



    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = YouTubeSettings()
