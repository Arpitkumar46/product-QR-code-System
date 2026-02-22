import os
from io import BytesIO
from datetime import datetime
import qrcode
from qrcode.constants import ERROR_CORRECT_M
from PIL import Image

def generate_qr_bytes(url: str, box_size: int = 10, border: int = 4) -> bytes:
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.read()

def save_qr_file(url: str, product_id: str, folder: str, box_size: int = 10) -> str:
    os.makedirs(folder, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = f"{product_id}_{ts}.png"
    path = os.path.join(folder, filename)
    data = generate_qr_bytes(url, box_size=box_size)
    with open(path, "wb") as f:
        f.write(data)
    return path
