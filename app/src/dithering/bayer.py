import numpy as np
from scipy.spatial import KDTree
import math
from app.src.dithering.nns import findClosestColor


def bitInterleave(a, b):
    """ Interleave bits of two numbers. """
    result = 0
    shift = 0
    nums = [a, b]
    while nums[0] or nums[1]:
        # switch between bits from a and b
        for n in range(2):
            bit = (nums[n] & 1) << shift
            result |= bit
            nums[n] >>= 1
            shift += 1
    return result


def reverseBits(a):
    """ Reverse order of bits in a number. """
    result = 0
    shift = a.bit_length()
    while shift:
        shift -= 1
        result |= ((a >> shift) & 1) << (a.bit_length() - shift - 1)

    return result


def generateTresholdMap(n: int) -> np.ndarray:
    """ Generate Bayer threshold map with a given size. """
    tresholdMap = np.zeros((n, n), dtype=np.float64)
    for y in range(n):
        for x in range(n):
            if y < n // 2:
                tresholdMap[y, x] = reverseBits(
                    bitInterleave((y + n//2) ^ x, y + n//2))
                if x < n // 2:
                    tresholdMap[y, x] -= 3
                else:
                    tresholdMap[y, x] += 1
            else:
                tresholdMap[y, x] = reverseBits(
                    bitInterleave(y ^ x, y))
    tresholdMap = (tresholdMap + 1) / n**2 - 0.5
    return tresholdMap


def dither(img: np.ndarray, palette: np.ndarray, n: int) -> np.ndarray:
    """Dither image using Bayer algorithm.

    Args:
        img (np.ndarray): image to dither
        palette (np.ndarray): color palette to pick from
        n (int): size of threshold map

    Returns:
        np.ndarray: dithered image
    """
    paletteTree = KDTree(palette)
    tresholdMap = generateTresholdMap(n)
    spread = 255 / (2*math.log(palette.size, 2)/3)
    img = img.astype(np.float)
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            img[y, x] += tresholdMap[y % n, x % n] * spread
            img[y, x] = findClosestColor(img[y, x], palette, paletteTree)
    return img
