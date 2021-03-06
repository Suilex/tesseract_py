import os

import pytesseract
from PIL import Image
from connect_db import add_to_db
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'
MAIN_FOLDER = r'D:\armd\httpd-2.4.23-win64\Apache24\htdocs\armd\web\scans'


def tesseract_extract_img(file, deal_id, user_id, indictment):
    img = Image.open(file)
    data = pytesseract.image_to_string(img, lang='rus')
    add_to_db(deal_id, user_id, data, indictment)


def tesseract_extract_pdf(file, deal_id, user_id, indictment):
    data = ""
    for img in convert_from_path(file):
        data += pytesseract.image_to_string(img, lang='rus')
    add_to_db(deal_id, user_id, data, indictment)


def main():
    for folder in os.listdir(MAIN_FOLDER):
        deal_id, user_id = folder.split('_')[:2]
        indictment = len(folder.split('.')) == 2
        path_of_folder = os.path.join(MAIN_FOLDER, folder)
        for file in os.listdir(path_of_folder):
            path_of_file = os.path.join(path_of_folder, file)
            extension = file.split('.')[-1].lower()
            if extension == 'jpg' or extension == 'jpeg':
                tesseract_extract_img(path_of_file, deal_id, user_id, indictment)
            elif extension == 'pdf':
                tesseract_extract_pdf(path_of_file, deal_id, user_id, indictment)
            else:
                pass
            os.remove(path_of_file)
        os.rmdir(path_of_folder)


if __name__ == '__main__':
    main()
