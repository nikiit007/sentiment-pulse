from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
from datetime import datetime, timedelta
import json

class YouTubeSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        enable_decoding=False,
    )

    YOUTUBE_API_KEY: Optional[str] = None
    YT_SEARCH_TERMS: List[str] = ["Your Show trailer", "Your Show review"]
    YT_PUBLISHED_AFTER: str = (datetime.now() - timedelta(days=7)).isoformat()
    YT_MAX_VIDEOS: int = 25
    YT_MAX_COMMENTS_PER_VIDEO: int = 200
    DEMO_MODE: bool = False

    @field_validator("YT_SEARCH_TERMS", mode="before")
    def parse_search_terms(cls, value):
        """Accept JSON lists or comma-separated strings for search terms."""
        if value is None:
            return value
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return []
            if value.startswith("["):
                try:
                    loaded = json.loads(value)
                    if isinstance(loaded, list):
                        return loaded
                except json.JSONDecodeError:
                    pass
            # Fall back to comma-separated values
            return [term.strip() for term in value.split(",") if term.strip()]
        return value


settings = YouTubeSettings()
