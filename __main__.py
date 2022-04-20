from PIL import Image
from pathlib import Path
import numpy as np

from app.src.colorpalette import median_cut
from app.src.dithering import floyd_steinberg

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

# dither the image
imgDith = floyd_steinberg.dither(imgData, palette)

# show the image
Image.fromarray(imgDith.astype(np.uint8), 'RGB').show()
