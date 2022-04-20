from PIL import Image
from pathlib import Path
import numpy as np
from scipy.spatial import KDTree

from app.src.colorpalette import median_cut

# path to the input image
IMAGE_NAME = 'holenda'
IMAGE_EXT = '.jpg'
currentDir = Path(__file__).resolve().parent
imgPath = currentDir / 'example' / 'inputImages' / (IMAGE_NAME + IMAGE_EXT)

# load image to numpy array
with Image.open(imgPath) as img:
    imgData = np.asarray(img)

# get color palette
palette = median_cut.generate(imgData, 5)

# kdtree
paletteTree = KDTree(palette)
i = paletteTree.query([255, 255, 255])[1]
print(palette[i])

# show the image
Image.fromarray(imgData.astype(np.uint8), 'RGB').show()
