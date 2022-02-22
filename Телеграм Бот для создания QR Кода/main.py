import qrcode
from PIL import Image, ImageDraw
from pyzbar.pyzbar import decode
from path import Path


# Путь до картинки с QR кодом
def read_qr_code(path_to_download: Path):
    try:
        img = Image.open(path_to_download)
        decoded = decode(img)
        wrote = decoded[0].data.decode("utf-8")
    except Exception:
        wrote = None
    return wrote


def gen_qr_code(text: str, path_to_download: Path, path_to_save: Path = None):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.get_matrix()

    coeff = 20
    coeff_small = round(coeff / 3)
    length_qr = len(img) * coeff
    
    try:
        background = Image.open(path_to_download).resize((length_qr, length_qr)).convert("RGBA")
    except Exception:
        return False

    back_im = Image.new('RGBA', (length_qr, length_qr), (0, 0, 0, 0))
    black = (0, 0, 0, 230)
    white_1 = (255, 255, 255, 50)
    white_2 = (255, 255, 255, 230)
    idraw = ImageDraw.Draw(back_im, "RGBA")
    x = 0
    y = 0

    for string in qr.get_matrix():
        this_str = ''
        for i in string:
            if i:
                this_str += '1'
                idraw.rectangle((x + coeff_small, y + coeff_small, x + coeff - coeff_small, y + coeff - coeff_small),
                                fill=black)
            else:
                this_str += '0'
                idraw.rectangle((x + coeff_small, y + coeff_small, x + coeff - coeff_small, y + coeff - coeff_small),
                                fill=white_2)
            x += coeff
        x = 0
        y += coeff

    idraw.rectangle((0, 0, coeff * 9, coeff * 9), fill=white_1)
    idraw.rectangle((length_qr, 0, length_qr - coeff * 9, coeff * 9), fill=white_1)
    idraw.rectangle((0, length_qr, coeff * 9, length_qr - coeff * 9), fill=white_1)
    idraw.rectangle((length_qr - coeff * 10, length_qr - coeff * 9, length_qr - coeff * 6, length_qr - coeff * 6),
                    fill=white_1)
    idraw.rectangle((coeff, coeff, coeff * 8, coeff * 2), fill=black)
    idraw.rectangle((length_qr - coeff * 8, coeff, length_qr - coeff, coeff * 2), fill=black)
    idraw.rectangle((coeff, coeff * 7, coeff * 8, coeff * 8), fill=black)
    idraw.rectangle((length_qr - coeff * 8, coeff * 7, length_qr - coeff, coeff * 8), fill=black)
    idraw.rectangle((coeff, length_qr - coeff * 7, coeff * 8, length_qr - coeff * 8), fill=black)
    idraw.rectangle((coeff, length_qr - coeff * 2, coeff * 8, length_qr - coeff), fill=black)
    idraw.rectangle((length_qr - coeff * 7, length_qr - coeff * 7, length_qr - coeff * 8, length_qr - coeff * 8),
                    fill=black)
    idraw.rectangle((coeff * 3, coeff * 3, coeff * 6, coeff * 6), fill=black)
    idraw.rectangle((length_qr - coeff * 3, coeff * 3, length_qr - coeff * 6, coeff * 6), fill=black)
    idraw.rectangle((coeff * 3, length_qr - coeff * 3, coeff * 6, length_qr - coeff * 6), fill=black)
    idraw.rectangle((coeff, coeff, coeff * 2, coeff * 8), fill=black)
    idraw.rectangle((coeff * 7, coeff, coeff * 8, coeff * 8), fill=black)
    idraw.rectangle((length_qr - coeff, coeff, length_qr - coeff * 2, coeff * 8), fill=black)
    idraw.rectangle((length_qr - coeff * 7, coeff, length_qr - coeff * 8, coeff * 8), fill=black)
    idraw.rectangle((coeff, length_qr - coeff, coeff * 2, length_qr - coeff * 8), fill=black)
    idraw.rectangle((coeff * 7, length_qr - coeff, coeff * 8, length_qr - coeff * 8), fill=black)
    idraw.rectangle((length_qr - coeff * 10, length_qr - coeff * 10, length_qr - coeff * 9, length_qr - coeff * 5),
                    fill=black)
    idraw.rectangle((length_qr - coeff * 6, length_qr - coeff * 10, length_qr - coeff * 5, length_qr - coeff * 5),
                    fill=black)
    idraw.rectangle((length_qr - coeff * 6, length_qr - coeff * 10, length_qr - coeff * 10, length_qr - coeff * 9),
                    fill=black)
    idraw.rectangle((length_qr - coeff * 6, length_qr - coeff * 6, length_qr - coeff * 10, length_qr - coeff * 5),
                    fill=black)
    background.paste(back_im, (0, 0), back_im)
    if path_to_save is not None:
        path_to_download = path_to_save

    background.save(path_to_download)
    return True
