import numpy as np
from scipy.spatial import KDTree


def findClosestColor(pixel: np.ndarray, palette: np.ndarray,
                     paletteTree: KDTree) -> np.ndarray:
    """Find closest color in color palette.

    Args:
        pixel (np.ndarray): original color
        palette (np.ndarray): color palette
        paletteTree (KDTree): octree with the same color palette

    Returns:
        np.ndarray: closest color from the color palette
    """
    index = paletteTree.query(pixel)[1]
    return palette[index]


def applyError(error: np.ndarray, pixel: np.ndarray,
               distribution: float) -> np.ndarray:
    """Apply color quantization error to a pixel.

    Args:
        error (int): quantization error
        pixel (np.ndarray): color pixel to change
        distribution (float): coefficient of quantization error

    Returns:
        np.ndarray: new color value of the pixel
    """
    error = distribution * error
    error = np.around(error, decimals=0)
    newShade = pixel + error
    newShade = newShade.clip(0, 255)
    return newShade


def dither(img: np.ndarray, palette: np.ndarray) -> np.ndarray:
    """Dither image using Floyd-Steinberg algorithm.

    Args:
        img (np.ndarray): image to dither
        palette (np.ndarray): color palette to use

    Returns:
        np.ndarray: dithered image
    """
    # numbers won't stay positive during the dithering process
    img = img.astype(np.int16)
    height, width, _ = img.shape

    # construct octree data structure for quick nearest neighbour search
    paletteTree = KDTree(palette)

    for y in range(height):
        for x in range(width):
            old = img[y, x]
            new = findClosestColor(old, palette, paletteTree)
            error = old - new
            img[y, x] = new

            # apply quantization error to neighbours with the
            # following distribution:
            #                 current   7/16
            #         3/16     5/16     1/16

            # top right
            if x + 1 < width:
                img[y, x+1] = applyError(error, img[y, x+1], 7/16)
            # bottom
            if y + 1 < height:
                # left
                if x - 1 > 0:
                    img[y+1, x-1] = applyError(error, img[y+1, x-1], 3/16)

                # middle
                img[y+1, x] = applyError(error, img[y+1, x], 5/16)

                # right
                if x + 1 < width:
                    img[y+1, x+1] = applyError(error, img[y+1, x+1], 1/16)
    return img
