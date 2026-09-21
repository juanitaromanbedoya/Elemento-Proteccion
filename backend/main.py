from fastapi import FastAPI

app = FastAPI(title="EPP Verificador API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "EPP Verificador API - FastAPI"}