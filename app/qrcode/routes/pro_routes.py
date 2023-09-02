from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from ..schemas import ProUserConfigration
from ..utils import generate_pro_qr, generate_pro_qr_uri

router = APIRouter(
    prefix="/pro/qrcode",
    tags=["premium apis for qrcode"],
)


@router.post("/generate-uri")
def generate_pro_qrcode_uri(data: ProUserConfigration) -> dict:
    """
    Generate a QR code as PNG Data URI for the given data.
    """
    qrcode = generate_pro_qr_uri(data)
    return {
        "image": qrcode,
    }


@router.post("/generate")
def generate_pro_qrcode_image_post(data: ProUserConfigration) -> StreamingResponse:
    """
    Generate a QR code for the given data.
    """
    buff = generate_pro_qr(data)
    return StreamingResponse(buff, media_type=data.media_type)
