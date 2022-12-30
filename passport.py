import os
import sys
import json
from passporteye import read_mrz
from PIL import Image
import pytesseract
import cv2
import numpy as np
import re
from country_json import *


def clean_name(name):
    pattern = re.compile('([^\s\w]|_\<)+')
    name = pattern.sub('', name)
    return name.strip()

def mrz_parser(file_path):

    # Extract informations with PassportEye
    from passporteye import read_mrz
    
    file_path = sys.argv[1]
    if not file_path:
        return print("no file given")

    # Process image
    mrz = read_mrz(file_path)

    if mrz is None:
        return print("Can not read image")

    mrz_data = mrz.to_dict()

    user_info = {}
    user_info['last_name'] = mrz_data.get('surname').upper()
    user_info['first_name'] = clean_name(mrz_data.get('names').upper())
    user_info['country_code'] = mrz_data.get('country')
    user_info['country'] = get_country_name(user_info.get('country_code'))
    user_info['nationality'] = get_country_name(mrz_data.get('nationality'))
    user_info['number'] = clean_name(mrz_data.get('number'))
    user_info['sex'] = mrz_data.get('sex')
    valid_score = mrz_data.get('valid_score')
    return user_info


if __name__ == "__main__":
    file_path = sys.argv[1]
    result = mrz_parser(file_path)
    print(result)
