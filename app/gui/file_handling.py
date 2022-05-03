from tkinter import filedialog as fd
from PIL import Image
import numpy as np
import re


def selectFile(self) -> None:
    """ Show file selection dialog and load selected image. """

    # supported types used for type filtering in file selection dialog
    fileTypes = (
        ('all files', '*'),
        ('jpg image', '*.jpg'),
        ('jpeg image', '*.jpeg'),
        ('png image', '*.png'),
        ('tiff image', '*.tiff'),
        ('bmp image', '*.bmp'),
        ('gif image', '*.gif')
    )

    # show file dialog
    self.filePath = fd.askopenfilename(
        title='Select image',
        filetypes=fileTypes
    )

    # try to load image if file was selected
    if self.filePath:
        fileNameShort = re.findall(r'/[^/]+$', self.filePath)[0][1:]
        self.l_selectedFile.config(text=fileNameShort)
        self._loadImage()


def loadImage(self) -> None:
    """ Try to load image from selected file path. """

    # save old image data
    if self.imgData is not None:
        oldImgData = self.imgData.copy()

    # try opening image and loading it into numpy array
    try:
        with Image.open(self.filePath) as img:
            self.imgData = np.asarray(img)

        # remove alpha channel
        if self.imgData.shape[2] == 4:
            self.imgData = self.imgData[:, :, :3]

        # display image on cavas
        self._displayImageFromArray(self.imgData)

        # update button states
        self.b_submit["text"] = "Dither"
        self.b_submit["state"] = "active"
        self.l_submit["text"] = ""
        self.b_reset["state"] = "active"

    # error while opening file or loading it into array => invalid file
    except Exception:
        self.l_selectedFile.config(text="Invalid file.")
        self.b_submit["state"] = "disabled"
        self.imgData = oldImgData


def saveImage(self) -> None:
    """ Save dithered image to selected file path. """

    # try saving image to desired file path
    try:
        # ask for file saving location (creates the file)
        file = fd.asksaveasfile(mode='w', defaultextension=".png")
        if file is None:
            return
        file.close()

        # save image to newly created file
        img = Image.fromarray(self.imgDith.astype(np.uint8), 'RGB')
        img.save(file.name)

        # display message on the ui
        self.l_submit["text"] = "Image saved."

    # Error while writing file => invalid saving location
    except Exception:
        self.l_submit["text"] = "Invalid location."
