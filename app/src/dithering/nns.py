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
