from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from services.epp_detector import detect_epp

router = APIRouter(prefix="/api/v1", tags=["epp"])

class EPPDetectionResponse(BaseModel):
    helmet_detected: bool
    mask_detected: bool
    status: str

@router.post("/detect-epp", response_model=EPPDetectionResponse)
async def detect_epp_endpoint(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = detect_epp(image_bytes)
    return EPPDetectionResponse(**result)