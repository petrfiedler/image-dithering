from app.src.colorpalette import (
    median_cut,
    bit_stripping,
    constants
)
from app.src.dithering import (error_diffusion, bayer)
from threading import Thread
import sys


class KThread(Thread):
    """ Modify Thread class to support killing method. """
    # hack from: https://blog.finxter.com/how-to-kill-a-thread-in-python/

    def __init__(self, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self.killed = False

    def start(self):
        # replace the default run method
        self.runOld = self.run
        self.run = self.runWithTrace
        Thread.start(self)

    def runWithTrace(self):
        sys.settrace(self.globaltrace)
        self.runOld()
        self.run = self.runOld

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


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

    self.process = KThread(target=self._processImage, daemon=True)
    self.process.start()


def processingDone(self):
    self.b_selectFile["state"] = "active"
    self.b_submit["text"] = "Save Image"
    self.b_submit["state"] = "active"
    self.l_submit["text"] = "Dithering done."

    self._displayImageFromArray(self.imgDith)


def processImage(self):
    # get color palette
    if self.pickedPalette.get() == "Bit Stripping":
        palette = bit_stripping.generate(
            self.imgData, self.s_palleteOptions.get())

    elif self.pickedPalette.get() == "Websafe":
        palette = constants.WEBSAFE_PALETTE

    elif self.pickedPalette.get() == "Median Cut":
        palette = median_cut.generate(
            self.imgData, self.s_palleteOptions.get())

    else:
        raise NotImplementedError("No support for this color palette.")

    # dither the image
    if self.pickedDithering.get() == "Error Diffusion":
        map = self.pickedDitheringOption.get()
        self.imgDith = error_diffusion.dither(self.imgData, palette, map)

    elif self.pickedDithering.get() == "Bayer":
        self.imgDith = bayer.dither(
            self.imgData, palette, 2**self.s_ditheringOptions.get())

    self._processingDone()


def reset(self):
    if self.b_submit["text"] == "Processing...":
        self.process.kill()
    elif self.imgData is not None:
        self._displayImageFromArray(self.imgData)
    else:
        return
    self.b_submit["text"] = "Dither"
    self.b_submit["state"] = "active"
    self.l_submit["text"] = ""
    self.b_selectFile["state"] = "active"
