import pytest
import numpy as np

from tests.utils import loadImg

from app.src.colorpalette import (
    bit_stripping,
    median_cut
)


@pytest.fixture
def image_white():
    return loadImg("tests/img/white.png")


@pytest.fixture
def image_oneRedPixel():
    return loadImg("tests/img/red_pixel.png")


@pytest.fixture
def image_colorMap():
    return loadImg("tests/img/color_map.jpg")


# median cut:

@pytest.mark.parametrize(
    'input, reference',
    [
        ([
            [0, 0, 0],
            [255, 0, 0]
        ], 0),
        ([
            [0, 0, 0],
            [0, 0, 0]
        ], 0),
        ([
            [0, 0, 255],
            [0, 0, 0]
        ], 2),
        ([
            [244, 244, 255],
            [0, 0, 0]
        ], 2),
        ([
            [238, 244, 212],
            [64, 125, 89],
            [86, 188, 216],
            [76, 144, 108],
            [89, 25, 97],
            [166, 69, 126],
            [124, 76, 169],
            [2, 1, 6]
        ], 1)
    ])
def test_findMaxRange(input, reference):
    input = np.array(input)
    assert(median_cut.findMaxRange(input) == reference)


@pytest.mark.parametrize(
    'input, reference',
    [
        ([
            [
                [0, 0, 0],
                [255, 0, 0]
            ], [
                [0, 0, 0],
                [0, 0, 0]
            ], [
                [0, 0, 0],
                [0, 0, 0],
                [33, 66, 99]
            ]
        ], [
            [127, 0, 0],
            [0, 0, 0],
            [11, 22, 33]
        ]),
        ([
            [
                [1, 1, 1]
            ], [
                [2, 2, 2]
            ]
        ], [
            [1, 1, 1],
            [2, 2, 2]
        ])
    ])
def test_averageColors(input, reference):
    buckets = []
    for i in input:
        buckets.append(np.array(i))
    reference = np.array(reference)
    np.testing.assert_array_equal(median_cut.averageColors(buckets), reference)


def test_medianCutOneColor(image_white):
    palette = median_cut.generate(image_white, 5)
    np.testing.assert_array_equal(palette, np.array([[255, 255, 255]]))

    palette = median_cut.generate(image_white, 1)
    np.testing.assert_array_equal(palette, np.array([[255, 255, 255]]))


def test_medianCutOnePixel(image_oneRedPixel):
    palette = median_cut.generate(image_oneRedPixel, 5)
    np.testing.assert_array_equal(palette, np.array([[255, 0, 0]]))

    palette = median_cut.generate(image_oneRedPixel, 1)
    np.testing.assert_array_equal(palette, np.array([[255, 0, 0]]))


def test_medianCutSize(image_colorMap):
    palette = median_cut.generate(image_colorMap, 1)
    assert(palette.shape[0] == 2)

    palette = median_cut.generate(image_colorMap, 5)
    assert(palette.shape[0] == 2**5)


# bit stripping:

@pytest.mark.parametrize(
    'input, level, reference',
    [
        ([255, 255, 255], 1, [254, 254, 255]),
        ([255, 255, 255], 2, [253, 254, 254]),
        ([0, 0, 0], 5, [8, 6, 16]),
        ([0, 0, 0], 8, [64, 32, 128])
    ])
def test_stripper(input, level, reference):
    input = np.array(input)
    reference = np.array(reference)
    bit_stripping.stripper(input, level)
    np.testing.assert_array_equal(input, reference)


def test_bitStrippingOneColor(image_white):
    palette = bit_stripping.generate(image_white, 1)
    assert(palette.shape[0] == 1)


def test_bitStrippingOnePixel(image_oneRedPixel):
    palette = bit_stripping.generate(image_oneRedPixel, 1)
    assert(palette.shape[0] == 1)


def test_bitStrippingSize(image_colorMap):
    totalColors = np.unique(np.reshape(image_colorMap, (-1, 3)), axis=0)
    palette = bit_stripping.generate(image_colorMap, 1)
    assert(palette.shape[0] <= totalColors.shape[0])
