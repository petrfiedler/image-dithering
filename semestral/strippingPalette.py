from PIL import Image
import os
import numpy as np
import math
from medianCut import getColorPalette
from octree import Octree

# source: https://www.codeproject.com/Articles/109133/Octree-Color-Palette
LOSS_COMPENSATION = (
    (0,0,1,2,4,8,16,34,64),
    (0,0,2,2,4,6,12,12,32),
    (0,1,2,4,8,16,32,64,128)
)

def strippingPalette(im, level):
    def stripper(rgb):
        for i in range(3):
            # erase last n bits (given by level)
            rgb[i] >>= level
            rgb[i] <<= level
            # replace empty bits by constant
            rgb[i] += LOSS_COMPENSATION[i][level]

    pixels = np.array(im)
    pixels = pixels.reshape(-1,3)
    np.apply_along_axis(stripper, 1, pixels)
    pixels = np.unique(pixels, axis=0)
    return list(map(tuple, pixels))

    