
# YouTube Integration Setup and Usage

This document explains how to set up and use the YouTube integration for the Topic Trend & Sentiment Pulse MVP.

## Enabling the API

To enable the YouTube integration, you need to add your YouTube Data API v3 key to the `.env` file in the root of the project.

```
YOUTUBE_API_KEY=AIzaSyBXhKd7TPvOm0I4kgnvT8pifc0qQSKxUPw
```

## Configuring Terms and Date Window

You can configure the search terms and date window for fetching YouTube videos by setting the following environment variables in your `.env` file:

- `YT_SEARCH_TERMS`: A comma-separated list of search terms. Default: `"Your Show trailer,Your Show review"`
- `YT_PUBLISHED_AFTER`: The earliest date for videos to be published in ISO 8601 format. Default: 7 days ago.
- `YT_MAX_VIDEOS`: The maximum number of videos to fetch. Default: `25`
- `YT_MAX_COMMENTS_PER_VIDEO`: The maximum number of comments to fetch per video. Default: `200`

Alternatively, you can create a `data/ShowConfig.json` file to override the `YT_SEARCH_TERMS` from the environment variables:

```json
{
  "youtube_search_terms": ["My Awesome Show", "My Awesome Show review"]
}
```

## Running the Collector

### Manually

You can run the YouTube collector manually using the following command:

```bash
python -m backend.jobs.collect_youtube
```

### Via API

You can also trigger the collector by sending a POST request to the `/api/collect/youtube` endpoint:

```bash
curl -X POST http://127.0.0.1:8000/api/collect/youtube
```

## Output

The collected YouTube comments will be stored as NDJSON in `/data/raw/YYYY-MM-DD/youtube.ndjson`.

The downstream `enrich` and `aggregate` steps will automatically pick up the new data from this directory.

## Quota

The YouTube Data API has a quota for requests. The current implementation uses the `search.list` and `commentThreads.list` endpoints, which are relatively low-cost.

- `search.list`: 100 units per request
- `commentThreads.list`: 1 unit per request

You can monitor your quota usage in the Google Cloud Console. The free daily quota is 10,000 units, which should be sufficient for most use cases.
