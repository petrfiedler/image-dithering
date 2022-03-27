from PIL import Image
import os
import numpy as np
import math
from medianCut import getColorPalette
from octree import Octree

imgName = "arcus"
numberOfBits = 3


# open image
currentPath = os.path.dirname(os.path.realpath(__file__))
with Image.open(currentPath + "/inputImages/" + imgName + ".jpg") as im:
    # get color palette
    colorPalette = getColorPalette(im, numberOfBits)
    oct = Octree()
    for color in colorPalette:
        oct.addColor(color)
    oct.print()