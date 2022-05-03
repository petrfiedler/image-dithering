import numpy as np

from app.src.utils.killable_thread import KThread

from app.src.colorpalette import (
    median_cut,
    bit_stripping,
    constants
)

from app.src.dithering import (
    error_diffusion,
    bayer
)


def pressSubmit(self) -> None:
    """ Perform actions when submit button is pressed. """

    # "save image" state:
    if self.b_submit["text"] == "Save Image":
        self._saveImage()
        return

    # "process image" state:

    # update button states
    self.b_submit["text"] = "Processing..."
    self.b_submit["state"] = "disabled"
    self.b_selectFile["state"] = "disabled"
    self.l_submit["text"] = "This might take a while."

    # start processing thread
    self.process = KThread(target=self._processImage, daemon=True)
    self.process.start()


def processingDone(self):
    """ Actions to perform when image processing is done. """

    # update button states
    self.b_selectFile["state"] = "active"
    self.b_submit["text"] = "Save Image"
    self.b_submit["state"] = "active"
    self.l_submit["text"] = "Dithering done."

    # display dithered image
    self._displayImageFromArray(self.imgDith)


def processImage(self) -> None:
    """ Perform image processing. """

    # get color palette
    if self.pickedPalette.get() == "Bit Stripping":
        palette = bit_stripping.generate(
            self.imgData, self.s_palleteOptions.get())

    elif self.pickedPalette.get() == "Websafe":
        palette = constants.WEBSAFE_PALETTE

    elif self.pickedPalette.get() == "Median Cut":
        palette = median_cut.generate(
            self.imgData, self.s_palleteOptions.get())

    elif self.pickedPalette.get() == "Monochrome":
        palette = np.array([[0, 0, 0], [255, 255, 255]], dtype=np.uint8)

    else:
        palette = self.imgData.reshape(-1, 3)

    # copy image data
    imgToDither = np.copy(self.imgData)

    # convert to black and white if needed
    if self.pickedPalette.get() == "Monochrome":
        bnw = np.average(
            imgToDither, weights=[0.299, 0.587, 0.114], axis=2)
        imgToDither = np.dstack((bnw, bnw, bnw))

    # dither the image
    if self.pickedDithering.get() == "Error Diffusion":
        map = self.pickedDitheringOption.get()
        self.imgDith = error_diffusion.dither(imgToDither, palette, map)

    elif self.pickedDithering.get() == "Bayer":
        self.imgDith = bayer.dither(
            imgToDither, palette, 2**self.s_ditheringOptions.get())

    else:
        self.imgDith = imgToDither

    # show result in the ui
    self._processingDone()


def reset(self) -> None:
    """ Reset processed image. """

    # kill process if running
    if self.b_submit["text"] == "Processing...":
        self.process.kill()

    # reset displayed image
    elif self.imgData is not None:
        self._displayImageFromArray(self.imgData)

    else:
        return

    # reset button states
    self.b_submit["text"] = "Dither"
    self.b_submit["state"] = "active"
    self.l_submit["text"] = ""
    self.b_selectFile["state"] = "active"
