import numpy as np

# source: https://www.codeproject.com/Articles/109133/Octree-Color-Palette
LOSS_COMPENSATION = (
    (0, 0, 1, 2, 4, 8, 16, 34, 64),
    (0, 0, 2, 2, 4, 6, 12, 12, 32),
    (0, 1, 2, 4, 8, 16, 32, 64, 128)
)


def stripper(rgb: np.ndarray, level: int) -> None:
    """ Strip one pixel by level. """
    for i in range(3):
        # erase last n bits (given by level)
        rgb[i] >>= level
        rgb[i] <<= level
        # replace empty bits by constant
        rgb[i] += LOSS_COMPENSATION[i][level]


def generate(img: np.ndarray, level: int) -> np.ndarray:
    """Generate color palette by striping bits of color channel values
        and compensating them with constant value.


    Args:
        img (np.ndarray): image to generate palette from_
        level (int): number of bits to strip

    Returns:
        np.ndarray: color palette
    """
    pixels = np.copy(img).reshape(-1, 3)
    np.apply_along_axis(stripper, 1, pixels, level)
    pixels = np.unique(pixels, axis=0)
    return pixels
