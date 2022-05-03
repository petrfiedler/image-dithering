import pytest
import numpy as np
from scipy.spatial import KDTree

from tests.utils import loadImg

from app.src.dithering import (
    bayer,
    error_diffusion,
    nns
)


# Bayer dithering:

def test_bitInterleave():
    assert(bayer.bitInterleave(0, 0) == 0)
    assert(bayer.bitInterleave(1, 0) == 1)
    assert(bayer.bitInterleave(0, 1) == 2)
    assert(bayer.bitInterleave(1, 1) == 3)
    assert(bayer.bitInterleave(0b1011, 0b1100) == 0b11100101)
    assert(bayer.bitInterleave(0b11111, 0b0) == 0b101010101)


def test_reverseBits():
    assert(bayer.reverseBits(0) == 0)
    assert(bayer.reverseBits(1) == 1)
    assert(bayer.reverseBits(2) == 1)
    assert(bayer.reverseBits(3) == 3)
    assert(bayer.reverseBits(4) == 1)
    assert(bayer.reverseBits(0b10101) == 0b10101)
    assert(bayer.reverseBits(0b1011) == 0b1101)
    assert(bayer.reverseBits(0b1011010110110) == 0b110110101101)
    assert(bayer.reverseBits(0b1000000000000) == 0b1)


def test_generateTresholdMap():
    map2 = (np.array(
        [[0, 2],
         [3, 1]],
        dtype=np.float64
    ) + 1) / 2**2 - 0.5

    map4 = (np.array(
        [[0, 8, 2, 10],
         [12, 4, 14, 6],
         [3, 11, 1, 9],
         [15, 7, 13, 5]],
        dtype=np.float64
    ) + 1) / 4**2 - 0.5

    map8 = (np.array(
        [[0, 32, 8, 40, 2, 34, 10, 42],
         [48, 16, 56, 24, 50, 18, 58, 26],
         [12, 44, 4, 36, 14, 46, 6, 38],
         [60, 28, 52, 20, 62, 30, 54, 22],
         [3, 35, 11, 43, 1, 33, 9, 41],
         [51, 19, 59, 27, 49, 17, 57, 25],
         [15, 47, 7, 39, 13, 45, 5, 37],
         [63, 31, 55, 23, 61, 29, 53, 21]],
        dtype=np.float64
    ) + 1) / 8**2 - 0.5

    np.testing.assert_array_equal(bayer.generateTresholdMap(2), map2)
    np.testing.assert_array_equal(bayer.generateTresholdMap(4), map4)
    np.testing.assert_array_equal(bayer.generateTresholdMap(8), map8)


@pytest.fixture
def image_colorScale():
    return loadImg("tests/img/color_scale.png")


@pytest.fixture
def image_white():
    return loadImg("tests/img/white.png")


@pytest.fixture
def image_oneRedPixel():
    return np.load("tests/img/red_pixel.png")


@pytest.fixture
def palette_websafe():
    return np.load("app/src/colorpalette/constants/websafe.npy")


def test_bayerColorRange(image_colorScale):
    palette = np.array([[0, 0, 0], [255, 255, 255]], dtype=np.uint8)
    dithered = bayer.dither(image_colorScale, palette, 2)
    ditheredRange = np.reshape(dithered, (-1, 3))
    ditheredRange = np.unique(ditheredRange, axis=0)
    assert(ditheredRange.shape[0] <= 2)


def test_bayerOneColor(image_white, palette_websafe):
    dithered = bayer.dither(image_white, palette_websafe, 2)
    np.testing.assert_array_equal(dithered, image_white)


def test_bayerOnePixel(image_white, palette_websafe):
    dithered = bayer.dither(image_white, palette_websafe, 2)
    np.testing.assert_array_equal(dithered, image_white)


# Error diffusion dithering:

def test_applyErrorInt():
    oldPixel = np.array([0, 0, 0])
    error = np.array([1, 2, 3])
    distribution = 2
    newPixel = error_diffusion.applyError(error, oldPixel, distribution)
    np.testing.assert_array_equal(newPixel, np.array([2, 4, 6]))


def test_applyErrorFloat():
    oldPixel = np.array([0, 0, 0])
    error = np.array([1, 2, 3])
    distribution = 0.5
    newPixel = error_diffusion.applyError(error, oldPixel, distribution)
    np.testing.assert_array_equal(newPixel, np.array([0, 1, 2]))


def test_applyErrorNegative():
    oldPixel = np.array([100, 100, 100])
    error = np.array([-1, 0, 1])
    distribution = 5
    newPixel = error_diffusion.applyError(error, oldPixel, distribution)
    np.testing.assert_array_equal(newPixel, np.array([95, 100, 105]))


def test_errorColorRange(image_colorScale):
    palette = np.array([[0, 0, 0], [255, 255, 255]], dtype=np.uint8)
    dithered = error_diffusion.dither(
        image_colorScale, palette, "Floyd-Steinberg")
    ditheredRange = np.reshape(dithered, (-1, 3))
    ditheredRange = np.unique(ditheredRange, axis=0)
    assert(ditheredRange.shape[0] <= 2)


def test_errorOneColor(image_white, palette_websafe):
    dithered = error_diffusion.dither(
        image_white, palette_websafe, "Floyd-Steinberg")
    np.testing.assert_array_equal(dithered, image_white)


def test_errorOnePixel(image_white, palette_websafe):
    dithered = error_diffusion.dither(
        image_white, palette_websafe, "Floyd-Steinberg")
    np.testing.assert_array_equal(dithered, image_white)


# Nearest neighbour search

@pytest.fixture
def kdtree_websafe(palette_websafe):
    return KDTree(palette_websafe)


@pytest.mark.parametrize(
    'input, reference',
    [
        ([0, 0, 0], [0, 0, 0]),
        ([2, 2, 2], [0, 0, 0]),
        ([40, 38, 20], [51, 51, 0]),
        ([89, 75, 42], [102, 51, 51]),
        ([25, 25, 26], [0, 0, 51]),
        ([254, 254, 254], [255, 255, 255])
    ])
def test_nnsWebsafe(input, reference, kdtree_websafe, palette_websafe):
    input = np.array(input)
    reference = np.array(reference)
    nearest = nns.findClosestColor(input, palette_websafe, kdtree_websafe)
    print(nearest, reference)
    np.testing.assert_array_equal(nearest, reference)
