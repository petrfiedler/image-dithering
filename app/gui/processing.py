from app.src.colorpalette import median_cut
from app.src.dithering import floyd_steinberg
from threading import Thread


def pressSubmit(self):
    self.b_submit["text"] = "Processing..."
    self.b_submit["state"] = "disabled"

    process = Thread(target=self._processImage, daemon=True)
    process.start()


def processingDone(self):
    self.b_submit["text"] = "Dither"
    self.b_submit["state"] = "active"

    self._displayImageFromArray(self.imgDith)


def processImage(self):
    # ! ALGORITHM CHOICE NOT YET SUPPORTED
    # get color palette
    palette = median_cut.generate(self.imgData, 5)

    # dither the image
    self.imgDith = floyd_steinberg.dither(self.imgData, palette)

    self._processingDone()
