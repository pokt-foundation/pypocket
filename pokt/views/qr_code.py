from PIL import Image
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers import CircleModuleDrawer

import os

PKG_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
LOGO_PATH = os.path.join(PKG_DIR, "assets", "POKT_symbol_bg.png")


def make_pokt_qr(address: str) -> Image.Image:

    qr = qrcode.QRCode(error_correction=qrcode.ERROR_CORRECT_H)
    qr.add_data(address)

    qr_color = SolidFillColorMask(
        front_color=(29, 138, 237), back_color=(255, 255, 255)
    )
    return qr.make_image(
        image_factory=StyledPilImage,
        embeded_image_path=LOGO_PATH,
        module_drawer=CircleModuleDrawer(),
        color_mask=qr_color,
    ).convert("RGBA")


if __name__ == "__main__":
    qr = make_pokt_qr(
        "https://docs.google.com/forms/d/e/1FAIpQLSf6o6vrEDQ-QUQz5M1tQ76XGOOP47aInzM7dhKTMCuTmThF1w/viewform"
    )
    qr.save("triforce-1.png")
    qr = make_pokt_qr(
        "https://docs.google.com/forms/d/e/1FAIpQLSfYOK1xe4QBMBHWJjT7k2V0Ki-UvFsxOtZgaa4V2CuejVwlXQ/viewform"
    )
    qr.save("triforce-2.png")
