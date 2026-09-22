from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, detect
from auth.database import init_db

init_db()  # crea la tabla de usuarios si no existe

app = FastAPI(
    title="EPP Verificador API",
    description="API para verificar el uso de Elementos de Protección Personal (casco y tapabocas) mediante detección con YOLOv8.",
    version="1.0.0"
)
# ... el resto sigue igual

# Middleware CORS - permite que el frontend Django (puerto 8001) consuma esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001", "http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(detect.router)

@app.get("/")
def root():
    return {"message": "EPP Verificador API - FastAPI"}