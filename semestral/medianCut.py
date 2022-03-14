import os
from PIL import Image
import numpy as np

def findMaxRange(pixels):
    # transpose the array to [[all r],[all g],[all b]]
    pixels = pixels.transpose()

    # find ranges of rgb color channels
    ranges = []
    for i in range(3):
        maxValue = max(pixels[i])
        minValue =  min(pixels[i])
        colorRange = maxValue - minValue
        ranges.append(colorRange)

    # return the index of color channel with the greatest range
    return ranges.index(max(ranges))


def getAverageColor(bucket):
    average = np.mean(bucket, axis=0)
    average = [round(channel) for channel in average]
    return tuple(average)


def averageColors(buckets):
    colorPallete = []

    for bucket in buckets:
        average = getAverageColor(bucket)
        colorPallete.append(average)
    
    return colorPallete


def getColorPalette(im, bits):
    # convert image to numpy array
    pixels = np.array(im)
    # get 1d array of rgb
    pixels = pixels.reshape(-1,3)

    buckets = []
    newBuckets = np.array_split(pixels, 1)

    # iterate through bits
    for bit in range(bits):
        buckets = [bucket for bucket in newBuckets]
        newBuckets = []

        # number of buckets grows exponentially
        for bucket in buckets:
            maxRange = findMaxRange(bucket)

            # sort color values by index given by maxRange
            bucket = bucket[bucket[:,maxRange].argsort()]

            # cut the bucket in median
            newBuckets += np.array_split(bucket, 2)

    colorPallete = averageColors(newBuckets)

    return colorPallete

"""
# open image
currentPath = os.path.dirname(os.path.realpath(__file__))
with Image.open(currentPath + "/inputImages/arcus.jpg") as img:
    colorPalette = getColorPalette(img, 5)

    # show palette
    im = []
    for color in colorPalette:
        im += [[color for i in range(70)] for j in range(70)]
    im = np.array(np.uint8(im))
    im = Image.fromarray(im)
    img.show()
    im.show()

"""