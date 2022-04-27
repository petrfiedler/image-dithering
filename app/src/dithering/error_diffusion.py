import numpy as np
from app.src.dithering.error_diffusion_maps import ERROR_DIFFUSION_MAPS
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


def dither(img: np.ndarray, palette: np.ndarray, map: str) -> np.ndarray:
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

    distribution = ERROR_DIFFUSION_MAPS[map]

    for y in range(height):
        for x in range(width):
            old = img[y, x]
            new = findClosestColor(old, palette, paletteTree)
            error = old - new
            img[y, x] = new

            # iterate through distribution map, where diff is
            # coordinate difference between near pixel and current pixel
            for (diff, coef) in distribution.items():
                nearY = y + diff[0]
                nearX = x + diff[1]
                if (0 <= nearY < height) and (0 <= nearX < width):
                    img[nearY, nearX] = applyError(
                        error, img[nearY, nearX], coef)

    return img
