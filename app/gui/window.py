from tkinter import Tk

from app.gui import (
    layout,
    file_handling,
    image_view,
    control_panel,
    palette_picker,
    dithering_picker,
    processing,
    styles
)


class Window:
    """ User interface window class. """

    def __init__(self, name: str = "Window") -> None:
        # instance variables
        self.displayedImg = None
        self.imgData = None

        # initial settings
        self.root = Tk()
        self.root.title(name)
        self.root.geometry("1024x720")
        self.root.minsize(1024, 720)

        self._loadStyleConstants()

        # bind components
        self._configureFrames()
        self._bindCanvas()
        self._bindControlPanel()

        self._applyStyles()

        # bind events
        self.root.bind("<Configure>", self._windowResize)
        self.canvas.bind("<MouseWheel>", self._imageMouseWheel)
        self.canvas.bind("<Button-4>", self._imageMouseWheel)
        self.canvas.bind("<Button-5>", self._imageMouseWheel)

    def show(self) -> None:
        """ Show window with user interface. """

        self.root.mainloop()

    # import methods
    _configureFrames = layout.configureFrames

    _selectFile = file_handling.selectFile
    _loadImage = file_handling.loadImage
    _saveImage = file_handling.saveImage

    _bindCanvas = image_view.bindCanvas
    _renderImage = image_view.renderImage
    _displayImageFromArray = image_view.displayImageFromArray
    _setDefaultImgZoom = image_view.setDefaultImgZoom
    _cropOutOfRender = image_view.cropOutOfRender
    _imageMouseWheel = image_view.imageMouseWheel
    _windowResize = image_view.windowResize

    _bindFileSelector = control_panel.bindFileSelector
    _bindControlPanel = control_panel.bindControlPanel

    _bindPalettePicker = palette_picker.bindPalettePicker
    _updatePalettePicker = palette_picker.updatePalettePicker

    _bindDitheringPicker = dithering_picker.bindDitheringPicker
    _updateDitheringPicker = dithering_picker.updateDitheringPicker

    _bindSubmit = control_panel.bindSubmit
    _bindReset = control_panel.bindReset
    _bindButtons = control_panel.bindButtons

    _pressSubmit = processing.pressSubmit
    _processImage = processing.processImage
    _processingDone = processing.processingDone
    _reset = processing.reset

    _loadStyleConstants = styles.loadStyleConstants
    _applyStyles = styles.applyStyles
