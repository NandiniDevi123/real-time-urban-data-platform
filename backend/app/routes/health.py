from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {"message": "API is running. Go to /docs or /health"}

@router.get("/health")
def health():
    return {"status": "Backend running successfully"}