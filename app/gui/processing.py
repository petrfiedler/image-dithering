from app.src.colorpalette import median_cut
from app.src.dithering import floyd_steinberg
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
    # ! ALGORITHM CHOICE NOT YET SUPPORTED
    # get color palette
    palette = median_cut.generate(self.imgData, self.s_palleteOptions.get())
    # dither the image
    self.imgDith = floyd_steinberg.dither(self.imgData, palette)

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
