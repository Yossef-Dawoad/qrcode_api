from io import BytesIO

import segno
from segno import helpers

from .schemas import BaseUserConfigration, ProUserConfigration, vCardUserConfigration


def generate_qr(data: BaseUserConfigration) -> BytesIO:
    buff = BytesIO()

    segno.make(data.content, error=data.error_correction, micro=False).save(
        buff,
        kind=data.output_format,
        dark=data.color,
        scale=data.scale,
    )

    buff.seek(0)
    return buff


def generate_qr_uri(data: BaseUserConfigration) -> str:
    return segno.make(
        data.content, error=data.error_correction, micro=False,
    ).png_data_uri(
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
    return segno.make(
        data.content, error=data.error_correction, micro=False,
    ).png_data_uri(
        dark=data.color,
        light=data.background_color,
        scale=data.scale,
        border=data.border if not data.transparent else 0,
    )


def generate_pro_qr_vcard(data: vCardUserConfigration) -> BytesIO:
    buff = BytesIO()
    helpers.make_vcard(
        name=f'{data.last_name};{data.first_name}',
        displayname=f'{data.first_name} {data.last_name}' if data.displayname is None else data.displayname,
        email=data.email,
        url=data.website,
        phone=data.phone,
        workphone=data.workphone,
        fax=data.fax,
        memo=data.memo,
        title=data.job_title,
        photo_uri=data.photo_uri,
        birthday=data.birthday,
    ).save(
        buff,
        kind=data.output_format,
        dark=data.color,
        light=data.background_color,
        scale=data.scale,
        border=data.border if not data.transparent else 0,
    )
    buff.seek(0)
    return buff
