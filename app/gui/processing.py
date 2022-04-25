from app.src.colorpalette import median_cut
from app.src.dithering import floyd_steinberg
from threading import Thread


def pressSubmit(self):
    # save image
    if self.b_submit["text"] == "Save Image":
        self._saveImage()
        return

    # process image
    self.b_submit["text"] = "Processing..."
    self.b_submit["state"] = "disabled"
    self.b_selectFile["state"] = "disabled"
    self.l_submit["text"] = "This might take a while."

    process = Thread(target=self._processImage, daemon=True)
    process.start()


def processingDone(self):
    self.b_selectFile["state"] = "active"
    self.b_submit["text"] = "Save Image"
    self.b_submit["state"] = "active"
    self.l_submit["text"] = "Dithering done."

    self._displayImageFromArray(self.imgDith)


def processImage(self):
    # ! ALGORITHM CHOICE NOT YET SUPPORTED
    # get color palette
    palette = median_cut.generate(self.imgData, 5)

    # dither the image
    self.imgDith = floyd_steinberg.dither(self.imgData, palette)

    self._processingDone()
