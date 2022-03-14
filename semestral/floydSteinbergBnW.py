from PIL import Image
import os

def getShadeOfGray(r,g,b):
    grayScale = int(0.299*r + 0.587*g + 0.114*b)
    # source: http://support.ptc.com/help/mathcad/en/index.html#page/PTC_Mathcad_Help/example_grayscale_and_color_in_images.html
    return grayScale

def blackOrWhite(grayScale):
    bow = (grayScale >= 128)*255
    return bow

def applyError(error, rgb, distribution):
    newShade = int(rgb[0] + error * distribution)
    return (newShade, newShade, newShade)

currentPath = os.path.dirname(os.path.realpath(__file__))
with Image.open(currentPath + "/inputImages/holenda.jpg") as im:

    pixels = im.load()
    width, height = im.size

    # convert to grayScale
    for y in range(height):
        for x in range(width):
            shade = getShadeOfGray(*pixels[x,y])
            pixels[x,y] = (shade, shade, shade)

    # apply Floyd-Steinberg dithering
    for y in range(height):
        for x in range(width):
            old = pixels[x,y][0]
            new = blackOrWhite(old)
            pixels[x,y] = (new, new, new)
            error = old - new

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
                pixels[x,y+1] = applyError(error, pixels[x,y+1], 3/16)

                # right
                if x + 1 < width:
                    pixels[x+1,y+1] = applyError(error, pixels[x+1,y+1], 3/16)
                


    im.show()