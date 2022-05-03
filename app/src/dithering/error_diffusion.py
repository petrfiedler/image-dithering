import numpy as np
from scipy.spatial import KDTree

from app.src.dithering.error_diffusion_maps import ERROR_DIFFUSION_MAPS
from app.src.dithering.nns import findClosestColor


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


def dither(img: np.ndarray, palette: np.ndarray, diffusion: str) -> np.ndarray:
    """Dither image using error diffusion algorithm.

    Args:
        img (np.ndarray): image to dither
        palette (np.ndarray): color palette to use
        diffusion (str): name of error diffusion map

    Returns:
        np.ndarray: dithered image
    """

    # numbers won't stay positive during the dithering process
    img = img.astype(np.int16)
    height, width, _ = img.shape

    # construct octree data structure for quick nearest neighbour search
    paletteTree = KDTree(palette)

    distribution = ERROR_DIFFUSION_MAPS[diffusion]

    # iterate through image pixels
    for y in range(height):
        for x in range(width):

            old = img[y, x]
            new = findClosestColor(old, palette, paletteTree)

            error = old - new

            img[y, x] = new

            # iterate through distribution map, where diff is
            # coordinate difference between near pixel and current pixel
            for (diff, coef) in distribution.items():

                # location of near pixel to apply error to
                nearY = y + diff[0]
                nearX = x + diff[1]

                # apply error if in bounds
                if (0 <= nearY < height) and (0 <= nearX < width):
                    img[nearY, nearX] = applyError(
                        error,
                        img[nearY, nearX],
                        coef
                    )

    return img
