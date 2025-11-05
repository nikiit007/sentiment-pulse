import os
import pytest

from backend.models.config import YouTubeSettings


@pytest.fixture(autouse=True)
def clear_env(monkeypatch):
    """Ensure we start each test without leaking settings."""
    for key in ("YT_SEARCH_TERMS",):
        monkeypatch.delenv(key, raising=False)


def test_comma_separated_terms(monkeypatch):
    monkeypatch.setenv("YT_SEARCH_TERMS", "foo, bar, baz ")
    settings = YouTubeSettings()
    assert settings.YT_SEARCH_TERMS == ["foo", "bar", "baz"]


def test_json_list_terms(monkeypatch):
    monkeypatch.setenv("YT_SEARCH_TERMS", '["Sandman", "Dream"]')
    settings = YouTubeSettings()
    assert settings.YT_SEARCH_TERMS == ["Sandman", "Dream"]


def test_empty_string_terms(monkeypatch):
    monkeypatch.setenv("YT_SEARCH_TERMS", "")
    settings = YouTubeSettings()
    assert settings.YT_SEARCH_TERMS == []
