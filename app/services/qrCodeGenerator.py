import pyqrcode
from app.services.utils import getValue
import os


class QRCodeGenerator:

    def create(self, uuid, pin_code = None, scale=8) :
        path = getValue("path_qrcode")

        if not os.path.isdir(path) :
            os.makedirs(path)

        domain = getValue("domain")

        if pin_code is None:
            str = domain + uuid
        else:
            str = domain+uuid+"?pinCode="+pin_code
        url = pyqrcode.create(str)

        full_path_img = path + uuid + ".png"
        url.png(full_path_img, scale=scale)
        return full_path_img
