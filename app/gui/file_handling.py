import re
from tkinter import filedialog as fd
import numpy as np
from PIL import Image


def selectFile(self):
    fileTypes = (
        ('all files', '*'),
        ('jpg image', '*.jpg'),
        ('jpeg image', '*.jpeg'),
        ('png image', '*.png'),
        ('tiff image', '*.tiff'),
        ('bmp image', '*.bmp'),
        ('gif image', '*.gif')
    )

    self.filePath = fd.askopenfilename(
        title='Select image', filetypes=fileTypes)

    if self.filePath:
        fileNameShort = re.findall(r'/[^/]+$', self.filePath)[0][1:]
        self.l_selectedFile.config(text=fileNameShort)
        self._loadImage()


def loadImage(self):
    try:
        with Image.open(self.filePath) as img:
            self.imgData = np.asarray(img)
            self._displayImageFromArray(self.imgData)
            self.b_submit["state"] = "active"
    # TODO: more specific error messages
    except Exception as e:
        print(f"Error while selecting image: {e}")
        self.l_selectedFile.config(text="Invalid file!")
        self.b_submit["state"] = "disabled"
