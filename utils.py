"""
Helper and utiliy functions
"""
import numpy as np
from PIL import Image

def get_long(file_path: str) -> int:
    """Returns the starting point of longitude of an image"""
    longitude = int(file_path.split('_')[2]) * 1000
    return longitude

def get_lat(file_path: str) -> int:
    """Returns the starting point of latitude of an image"""
    latitude = int(file_path.split('_')[3]) * 1000
    return latitude

def load_img(files_path: str) -> np.array:
    img = np.array(Image.open(files_path).convert("RGB"))
    return img