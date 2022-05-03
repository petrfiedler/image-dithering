from PIL import Image
import numpy as np


def loadImg(filename):
    with Image.open(filename) as img:
        return np.array(img)
