import numpy as np


def findMaxRange(pixels: np.ndarray) -> int:
    """Find index of color channel with the greatest range.

    Args:
        pixels (np.ndarray): pixels to search at

    Returns:
        int: index of color channel
    """
    # find color ranges of each color channel
    maxChannels = pixels.max(axis=0)
    minChannels = pixels.min(axis=0)
    ranges = maxChannels - minChannels

    # return the index of color channel with the greatest range
    return np.argmax(ranges)


def averageColors(buckets: list) -> np.ndarray:
    """Generate color palette by averaging colors in each bucket.

    Args:
        buckets (list): numpy arrays with colors

    Returns:
        np.ndarray: color palette
    """
    palette = np.empty((1, 3), dtype=np.uint8)
    for bucket in buckets:
        average = np.mean(bucket, axis=0)
        palette = np.vstack([palette, average])
    palette = palette[1:, :]
    return palette.astype(np.uint8)


def generate(img: np.ndarray, bits: int) -> np.ndarray:
    """Generate color palette using median cut algorithm.

    Args:
        img (np.ndarray): image to process
        bits (int): number of splits

    Returns:
        np.ndarray: color palette
    """
    pixels = img.reshape(-1, 3)
    if pixels.size <= 2**bits:
        return pixels
    buckets = [pixels]

    # create 2**bits buckets (each iteration splits each bucket in half)
    for _ in range(bits):
        oldBuckets = [bucket for bucket in buckets]
        buckets = []

        # split each bucket in median
        for bucket in oldBuckets:
            maxRange = findMaxRange(bucket)
            # sort by the color channel with the greatest range
            bucket = bucket[bucket[:, maxRange].argsort()]
            splitBucket = np.array_split(bucket, 2)
            buckets += splitBucket

    palette = averageColors(buckets)
    return palette
