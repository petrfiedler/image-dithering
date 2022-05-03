import numpy as np
from PIL import Image, ImageTk
import math
from tkinter import Event, Canvas


def bindCanvas(self) -> None:
    """ Bind canvas element to main window. """

    self.canvas = Canvas(self.rFrame)
    self.canvas.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)


def displayImageFromArray(self, imgData: np.ndarray) -> None:
    """ Display image in form of np.ndarray on canvas. """

    # convert to PIL image
    self.displayedImgArray = imgData
    self.displayedImg = Image.fromarray(imgData.astype(np.uint8), 'RGB')

    # render with deafult zoom
    self._setDefaultImgZoom()
    self._renderImage()


def cropOutOfRender(self, img: Image) -> Image:
    """ Crop image from parts which won't render on canvas. """

    # image size
    iWidth = int(img.size[0] * self.imgZoom)
    iHeight = int(img.size[1] * self.imgZoom)

    # canvas size
    cWidth = self.canvas.winfo_width()
    cHeight = self.canvas.winfo_height()

    # crop if future image size is higher than canvas size
    if cWidth < iWidth:
        img = img.crop((
            math.floor(((iWidth - cWidth)/2)/self.imgZoom),
            0,
            math.ceil(((iWidth - cWidth)/2 + cWidth)/self.imgZoom),
            img.size[1]
        ))

    if cHeight < iHeight:
        img = img.crop((
            0,
            math.floor(((iHeight - cHeight)/2) / self.imgZoom),
            img.size[0],
            math.ceil(((iHeight-cHeight)/2+cHeight)/self.imgZoom)
        ))

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
    self.canvas.delete("all")

    photoImg = ImageTk.PhotoImage(img)

    imageid = self.canvas.create_image(
        self.canvas.winfo_width()/2,
        self.canvas.winfo_height()/2,
        anchor='center',
        image=photoImg
    )

    self.canvas.lower(imageid)
    self.canvas.imagetk = photoImg


def setDefaultImgZoom(self) -> None:
    """ Set image zoom to fit canvas the best. """

    # image size
    iWidth = self.displayedImg.size[0]
    iHeight = self.displayedImg.size[1]

    # canvas size
    cWidth = self.canvas.winfo_width()
    cHeight = self.canvas.winfo_height()

    # fit to width
    if cWidth / cHeight < iWidth / iHeight:
        self.imgZoom = cWidth / iWidth
    # fit to height
    else:
        self.imgZoom = cHeight / iHeight

    # if image enlarges, zoom by whole numbers to keep pixel borders
    if self.imgZoom > 1:
        self.imgZoom = math.floor(self.imgZoom)


def imageMouseWheel(self, event: Event) -> None:
    """ Zoom image in or out on mouse wheel. """

    if self.displayedImg is None:
        return

    # zoom out
    if event.num == 5 or event.delta == -120:
        # minimal displayed image size is 30 px
        if min(self.displayedImg.size) * self.imgZoom > 30:

            self.imgZoom /= 1.5

            # floor zoom to keep whole pixels if still zoomed in
            if self.imgZoom > 1:
                self.imgZoom = math.floor(self.imgZoom)

            self._renderImage()

    # zoom in
    if event.num == 4 or event.delta == 120:
        # maximal (theoretical) displayed image size is 30 000 px
        if max(self.displayedImg.size)*self.imgZoom < 30000:

            self.imgZoom *= 1.5

            # ceil zoom to keep whole pixels if zooming in
            if self.imgZoom > 1:
                self.imgZoom = math.ceil(self.imgZoom)

            self._renderImage()


def windowResize(self, _: Event) -> None:
    """ Adjust displayed image to resized window. """

    if self.displayedImg is not None:
        self._renderImage()
