import numpy as np
from PIL import Image, ImageTk
import math
from tkinter import Event


def displayImageFromArray(self, imgData: np.ndarray) -> None:
    """ Display image in form of np.ndarray on canvas. """
    self.displayedImgArray = imgData
    self.displayedImg = Image.fromarray(
        imgData.astype(np.uint8), 'RGB')
    self._setDefaultImgZoom()
    self._renderImage()


def cropOutOfRender(self, img: Image) -> Image:
    """ Crop image from parts which won't render on canvas. """
    iWidth = int(img.size[0] * self.imgZoom)
    iHeight = int(img.size[1] * self.imgZoom)
    cWidth = self.canvas.winfo_width()
    cHeight = self.canvas.winfo_height()
    # crop if future image size is higher than canvas size
    if cWidth < iWidth:
        img = img.crop((
            math.floor(((iWidth - cWidth)/2)/self.imgZoom),
            0,
            math.ceil(((iWidth - cWidth)/2 + cWidth)/self.imgZoom),
            img.size[1]))
    if cHeight < iHeight:
        img = img.crop((
            0,
            math.floor(((iHeight - cHeight)/2) / self.imgZoom),
            img.size[0],
            math.ceil(((iHeight-cHeight)/2+cHeight)/self.imgZoom)))
    return img


def renderImage(self) -> None:
    """ Render image on canvas based of image zoom. """
    # copy the original image
    img = self.displayedImg

    # crop the image where it doesn't render
    img = self._cropOutOfRender(img)

    # recalculate the image width and height
    newWidth = int(img.size[0] * self.imgZoom)
    newHeight = int(img.size[1] * self.imgZoom)

    # resize the image
    if self.imgZoom > 1:
        img = img.resize((newWidth, newHeight), resample=Image.NEAREST)
    # only downsized image can be smoothed out
    else:
        img = img.resize((newWidth, newHeight), Image.ANTIALIAS)

    # display on canvas
    photoImg = ImageTk.PhotoImage(img)
    self.canvas.delete("all")
    imageid = self.canvas.create_image(self.canvas.winfo_width()/2,
                                       self.canvas.winfo_height()/2,
                                       anchor='center',
                                       image=photoImg)
    self.canvas.lower(imageid)
    self.canvas.imagetk = photoImg


def setDefaultImgZoom(self) -> None:
    """ Set image zoom to fit canvas the best. """
    cWidth = self.canvas.winfo_width()
    cHeight = self.canvas.winfo_height()

    # fit to width
    if cWidth/cHeight < self.displayedImg.size[0]/self.displayedImg.size[1]:
        self.imgZoom = cWidth/self.displayedImg.size[0]
    # fit to height
    else:
        self.imgZoom = cHeight/self.displayedImg.size[1]

    # if image enlarges, zoom by whole numbers to keep pixel borders
    if self.imgZoom > 1:
        self.imgZoom = math.floor(self.imgZoom)


def imageMouseWheel(self, event: Event) -> None:
    """ Zoom image in or out on mouse wheel. """
    if self.displayedImg is None:
        return

    # zoom out
    if event.num == 5 or event.delta == -120:
        if min(self.displayedImg.size) * self.imgZoom > 30:
            self.imgZoom /= 1.5
            if self.imgZoom > 1:
                self.imgZoom = math.floor(self.imgZoom)
            self._renderImage()

    # zoom in
    if event.num == 4 or event.delta == 120:
        if max(self.displayedImg.size)*self.imgZoom < 30000:
            self.imgZoom *= 1.5
            if self.imgZoom > 1:
                self.imgZoom = math.ceil(self.imgZoom)
            self._renderImage()
