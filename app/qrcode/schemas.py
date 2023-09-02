from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, model_validator
from pydantic.functional_validators import AfterValidator


class ErrorLevel(str, Enum):
    LEVEL_L = "L"
    LEVEL_M = "M"
    LEVEL_H = "H"
    LEVEL_Q = "Q"


class OutputType(str, Enum):
    PNG_IMAGE = "png"


class ProOutputType(str, Enum):
    PNG_IMAGE = "png"
    SVG_IMAGE = "svg"
    PDF_DOCUMENT = "pdf"
    EPS_TYPE = "eps"
    PPM_TYPE = "ppm"
    XPM_TYPE = "xpm"


def check_size(v: Optional[int]) -> int:
    """scale 1 module == 10 pixels"""
    SCALE_LIMIT = 30
    assert (
        v is not None
    ) and 1 < v < SCALE_LIMIT, f"you entered scale ={v}, free qr-code generation have to be between 1 and {SCALE_LIMIT}"
    return v


class BaseUserConfigration(BaseModel):
    content: str
    scale: Annotated[Optional[int], AfterValidator(check_size)] = 10
    color: Optional[str] = "#000000"
    format: Optional[OutputType] = OutputType.PNG_IMAGE
    error_correction: Optional[ErrorLevel] = ErrorLevel.LEVEL_H
    media_type: str = "image/png"

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def set_response_media_type(self) -> "BaseUserConfigration":
        match self.format:
            case OutputType.PNG_IMAGE:
                self.media_type = "image/png"
            case _:
                raise NotImplementedError(
                    """
                    free version of the api expect 'PNG' as the only format type,
                    if you want format types like svg, pdf, eps, ... use pro version of the api
                    """,
                )
        return self


class ProUserConfigration(BaseUserConfigration):
    background_color: Optional[str] = "#ffffff"
    scale: Optional[int] = 20
    logo: Optional[str] = None
    border: Optional[int] = 4
    transparent: Optional[bool] = False
    output_format: Optional[ProOutputType] = ProOutputType.PNG_IMAGE

    @model_validator(mode="after")
    def set_borderto_zero(self) -> "ProUserConfigration":
        if self.transparent:
            self.border = 0
        return self

    @model_validator(mode="after")
    def set_response_media_type(self) -> "ProUserConfigration":
        match self.output_format:
            case ProOutputType.PNG_IMAGE:
                self.media_type = "image/png"
            case ProOutputType.PDF_DOCUMENT:
                self.media_type = "application/pdf"
            case ProOutputType.SVG_IMAGE:
                self.media_type = "image/svg+xml"
            case ProOutputType.JPEG_IMAGE:
                raise NotImplementedError("JPEG to be implemented use 'PNG' Instead")
            case _:
                raise ValueError(f"Invalid export_type: {self.output_format}")

        return self
