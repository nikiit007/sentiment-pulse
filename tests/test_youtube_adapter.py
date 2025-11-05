
import responses
import pytest
from backend.adapters.youtube import YouTubeAPI

@pytest.fixture
def youtube_api():
    return YouTubeAPI(api_key="test_key")

@responses.activate
def test_search_videos(youtube_api):
    responses.add(
        responses.GET,
        "https://www.googleapis.com/youtube/v3/search",
        json={
            "items": [
                {
                    "id": {"videoId": "video1"},
                    "snippet": {
                        "title": "Video 1",
                        "channelId": "channel1",
                        "publishedAt": "2025-10-28T00:00:00Z",
                    },
                }
            ],
            "nextPageToken": "next_page_token",
        },
        status=200,
    )
    responses.add(
        responses.GET,
        "https://www.googleapis.com/youtube/v3/search",
        json={
            "items": [
                {
                    "id": {"videoId": "video2"},
                    "snippet": {
                        "title": "Video 2",
                        "channelId": "channel2",
                        "publishedAt": "2025-10-27T00:00:00Z",
                    },
                }
            ]
        },
        status=200,
    )

    videos = youtube_api.search_videos(
        search_terms=["test"], published_after="2025-10-26T00:00:00Z", max_videos=2
    )

    assert len(videos) == 2
    assert videos[0]["videoId"] == "video1"
    assert videos[1]["videoId"] == "video2"

@responses.activate
def test_fetch_comment_threads(youtube_api):
    responses.add(
        responses.GET,
        "https://www.googleapis.com/youtube/v3/commentThreads",
        json={
            "items": [
                {
                    "snippet": {
                        "topLevelComment": {
                            "id": "comment1",
                            "snippet": {
                                "textDisplay": "This is a comment",
                                "authorDisplayName": "User1",
                                "likeCount": 10,
                                "publishedAt": "2025-10-28T01:00:00Z",
                            },
                        }
                    },
                    "replies": {
                        "comments": [
                            {
                                "id": "reply1",
                                "snippet": {
                                    "textDisplay": "This is a reply",
                                    "authorDisplayName": "User2",
                                    "likeCount": 5,
                                    "publishedAt": "2025-10-28T02:00:00Z",
                                },
                            }
                        ]
                    },
                }
            ]
        },
        status=200,
    )

    comments = youtube_api.fetch_comment_threads(video_id="video1", max_comments=2)

    assert len(comments) == 2
    assert comments[0]["id"] == "comment1"
    assert comments[1]["id"] == "reply1"
