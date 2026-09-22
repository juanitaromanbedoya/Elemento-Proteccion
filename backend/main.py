from fastapi import FastAPI
from routers import auth, detect

app = FastAPI(
    title="EPP Verificador API",
    description="API para verificar el uso de Elementos de Protección Personal (casco y tapabocas) mediante detección con YOLOv8.",
    version="1.0.0"
)
app.include_router(auth.router)
app.include_router(detect.router)

@app.get("/")
def root():
    return {"message": "EPP Verificador API - FastAPI"}