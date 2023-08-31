from io import BytesIO

import segno

from .schemas import BaseUserConfigration, ProUserConfigration


def generate_qr(data: BaseUserConfigration) -> BytesIO:
    buff = BytesIO()

    segno.make(data.content, error=data.error_correction, micro=False).save(
        buff,
        kind=data.format,
        dark=data.color,
        scale=data.scale,
    )

    buff.seek(0)
    return buff


def generate_qr_uri(data: BaseUserConfigration) -> str:
    return segno.make(data.content, error=data.error_correction, micro=False).png_data_uri(
        dark=data.color,
        scale=data.scale,
    )


####################### pro functions  #######################


def generate_pro_qr(data: ProUserConfigration) -> BytesIO:
    buff = BytesIO()
    segno.make(data.content, error=data.error_correction, micro=False).save(
        buff,
        kind=data.output_format,
        dark=data.color,
        light=data.background_color,
        scale=data.scale,
        border=data.border if not data.transparent else 0,
    )

    buff.seek(0)
    return buff


def generate_pro_qr_uri(data: ProUserConfigration) -> str:
    return (
        segno.make(data.content, error=data.error_correction, micro=False).png_data_uri(
            dark=data.color,
            light=data.background_color,
            scale=data.scale,
            border=data.border if not data.transparent else 0,
        )
    )