from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app import limiter

from ..schemas import BaseUserConfigration
from ..utils import generate_qr, generate_qr_uri

router = APIRouter(
    prefix="/qrcode",
    tags=["free apis for qrcode "],
)


@router.post("/generate-uri")
@limiter.limit("80/hour;300/day")
def generate_qrcode_uri(request: Request, data: BaseUserConfigration) -> dict[str, str]:
    """
    Generate a QR code as PNG Data URI for the given data.
    """
    qrcode = generate_qr_uri(data)
    return {
        "image": qrcode,
    }


@router.post("/generate")
@limiter.limit("80/hour;300/day")
def generate_qrcode_image_post(request: Request, data: BaseUserConfigration) -> StreamingResponse:
    """
    Generate a QR code for the given data.
    """
    buff = generate_qr(data)
    return StreamingResponse(buff, media_type=data.media_type)
