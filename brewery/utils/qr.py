import base64
from io import BytesIO

import qrcode


def make_qr(data: str) -> str:
    img = qrcode.make(data)

    buffer = BytesIO()
    img.save(buffer, format='PNG')

    encoded = base64.b64encode(buffer.getvalue()).decode()

    return f'data:image/png;base64,{encoded}'
