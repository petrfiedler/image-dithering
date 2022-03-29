from PIL import Image
import os
import numpy as np
import math
from strippingPalette import strippingPalette

imgName = "colors"
strippingLevel = 5

def applyError(error, rgb, distribution):
    error = distribution * np.array(error)
    error = np.around(error, decimals=0)
    error = error.astype(int)
    newShade = np.add(error, rgb)
    return tuple(newShade)


def findClosestColor(pixel, colorPalette):
    shortestDistance = float('inf')
    for color in colorPalette:
        distance = math.dist(pixel, color)
        if distance < shortestDistance:
            closestColor = color
            shortestDistance = distance
    return closestColor


# open image
currentPath = os.path.dirname(os.path.realpath(__file__))
with Image.open(currentPath + "/inputImages/" + imgName + ".jpg") as im:
    # resize image
    newWidth = 256
    percentWidth = (newWidth/float(im.size[0]))
    newHeight = int((float(im.size[1])*float(percentWidth)))
    # im = im.resize((newWidth,newHeight), Image.ANTIALIAS)

    # get color palette
    colorPalette = strippingPalette(im, strippingLevel)
    print(f"Palette size: {len(colorPalette)}")
    pixels = im.load()
    width, height = im.size

    # apply Floyd-Steinberg dithering
    for y in range(height):
        for x in range(width):
            old = pixels[x,y]
            new = findClosestColor(old, colorPalette)
            pixels[x,y] = new
            error = np.subtract(old, new)

            # apply quantization error to neighbours with the following distribution :
            #                 current   7/16
            #         3/16     5/16     1/16

            # middle right
            if x + 1 < width:
                pixels[x+1,y] = applyError(error, pixels[x+1,y], 7/16)

            # bottom
            if y + 1 < height:
                # left
                if x - 1 > 0:
                    pixels[x-1,y+1] = applyError(error, pixels[x-1,y+1], 3/16)
                
                # middle
                pixels[x,y+1] = applyError(error, pixels[x,y+1], 5/16)

                # right
                if x + 1 < width:
                    pixels[x+1,y+1] = applyError(error, pixels[x+1,y+1], 1/16)

    im = im.save(currentPath + "/outputImages/" + imgName + "Stripping.png")