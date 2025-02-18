"""
Здесь происходит логика обработки изображения
"""
import os
import re
from typing import Optional

from PIL import Image, ImageFilter

from config import app


def blur_image(src_filename: str, dst_filename: Optional[str] = None):
    """
    Функция принимает на вход имя входного и выходного файлов.
    Применяет размытие по Гауссу со значением 5.
    """
    if not dst_filename:
        filename = re.findall(r'\d[^\\/]*$', src_filename)[-1]
        dst_filename = os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], f'blur_{filename}')

    with Image.open(src_filename) as img:
        img.load()
        new_img = img.filter(ImageFilter.GaussianBlur(5))
        new_img.save(dst_filename)

    return dst_filename
