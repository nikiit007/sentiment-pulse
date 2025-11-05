
from fastapi import APIRouter
from backend.jobs import collect_youtube

router = APIRouter()

@router.post("/api/collect/youtube")
def collect_youtube_data():
    result = collect_youtube.run_once()
    return result
