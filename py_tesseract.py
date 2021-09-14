import datetime
import os

import pytesseract
#from PIL.Image import core as _imaging
#from . import _imaging as core
from PIL import Image

from connect_db import add_to_db

tesseract_exe_location = r'D:\PythonMiniProjects\tesseract\Tesseract-OCR\tesseract.exe'
input_files_location = r'D:\www\Apache24\htdocs\armd\armd\web\scans'


class open_img:
    def __init__(self, file_path):
        self.file_path = file_path
        self.f = Image.open(file_path)

    def __enter__(self):
        return self.f

    def __exit__(self, *args):
        self.f.close()
        os.remove(self.file_path)


def convert_to_database(img):
    if img.size < (500, 500):
        print("Unreadable")
        return
    return pytesseract.image_to_string(img, lang="rus")


def to_path(*args):
    return "\\".join(args)


def to_start():
    log = ''
    for directory in os.listdir(path=input_files_location):
        for file in os.listdir(path=to_path(input_files_location, directory)):
            with open_img(to_path(input_files_location, directory, file)) as img:
                deal_id, user_id, _ = directory.split('_')
                log += 'day: {}   deal_id: {}   user_id: {}\n'.format(str(datetime.datetime.now()), deal_id, user_id)
                add_to_db(deal_id, user_id, convert_to_database(img))
        os.rmdir(path=to_path(input_files_location, directory))
    return log
