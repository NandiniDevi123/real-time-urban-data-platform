from fastapi import FastAPI

app = FastAPI(title="Real-Time Urban Data Integration & Analytics Platform")

@app.get("/")
def root():
    return {"message": "API is running. Go to /docs or /health"}

@app.get("/health")
def health():
    return {"status": "Backend running successfully"}