from pydantic import field_validator
from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class TestSettings(BaseSettings):
    YT_SEARCH_TERMS: List[str] = []

    @field_validator("YT_SEARCH_TERMS", mode="before")
    def split_search_terms(cls, v):
        if isinstance(v, str):
            return v.split(',')
        return v

print(f"YT_SEARCH_TERMS from env: {os.environ.get('YT_SEARCH_TERMS')}")
settings = TestSettings()
print(settings.YT_SEARCH_TERMS)
