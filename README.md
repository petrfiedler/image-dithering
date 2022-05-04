# Image Dithering - BI-PYT 2022 Semestral Project

## How To Use

1. Upload image you want to dither (smaller file sizes are recommended).
   Supported file types are:

    - png
    - jpg
    - tiff
    - bmp

2. Select color palette. You can specify options for certain color palettes.

3. Select dithering algorithm and specify options.

4. Dither.

5. Save your beautiful image.

6. If you want to dither the image with another settings, click 'Reset Image'.

You can zoom in and out in the image preview with mouse wheel to see the dithering effect.

## How To Run

Install Python environment and download the requirements.
In the project root directory, run:

```shellscript
pip install -r requirements.txt
```

This app was tested with Python 3.10.4 (older versions are not guaranteed to work properly).

After installing all the dependencies, you can run the app by running `__main__.py` in the project root directory. Or in the project directory, you can run:

```shellscript
python .
```

## Testing

Tests cover the significant parts of dithering and color quantization algorithms.

In the project root directory, run:

```shellscript
pytest
```
