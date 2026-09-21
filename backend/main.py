from fastapi import FastAPI
from routers import auth, detect

app = FastAPI(title="EPP Verificador API", version="1.0.0")
app.include_router(auth.router)
app.include_router(detect.router)

@app.get("/")
def root():
    return {"message": "EPP Verificador API - FastAPI"}