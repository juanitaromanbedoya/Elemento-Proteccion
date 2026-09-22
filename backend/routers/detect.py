from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from services.epp_detector import detect_epp
from schemas.epp_schema import EPPRulesResponse, EPPRule

router = APIRouter(prefix="/api/v1", tags=["epp"])

class EPPDetectionResponse(BaseModel):
    helmet_detected: bool
    mask_detected: bool
    status: str

@router.post(
    "/detect-epp",
    response_model=EPPDetectionResponse,
    summary="Detectar uso de EPP en una imagen",
    description="Recibe una imagen (captura de cámara) y retorna si la persona porta casco y tapabocas."
)
async def detect_epp_endpoint(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = detect_epp(image_bytes)
    return EPPDetectionResponse(**result)


EPP_RULES = [
    EPPRule(id=1, name="Casco de seguridad", required=True,
            description="Obligatorio en toda el área industrial para prevenir golpes en la cabeza."),
    EPPRule(id=2, name="Tapabocas", required=True,
            description="Obligatorio en zonas con exposición a polvo o partículas."),
]

@router.get(
    "/epp-rules",
    response_model=EPPRulesResponse,
    summary="Listar reglas de seguridad EPP",
    description="Retorna el listado de elementos de protección personal requeridos."
)
def get_epp_rules():
    return EPPRulesResponse(rules=EPP_RULES)