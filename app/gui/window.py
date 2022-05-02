from tkinter import (
    Tk,
    Frame
)

from app.gui import (
    file_handling,
    image_view,
    control_panel,
    palette_picker,
    dithering_picker,
    processing,
    styles
)


class Window:
    """ Context class for user interface window. """
    # imported methods
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

    def _configureFrames(self) -> None:
        """ Create main grid layout with frames. """
        # configure grid (1x3)
        self.root.grid_columnconfigure(0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # configure left frame (0, 0)
        self.lFrame = Frame(self.root, width=384)
        self.lFrame.grid(row=0, column=0,
                         sticky="nwe", padx=20, pady=20)

        # configure right frame (0, 1:2)
        self.rFrame = Frame(self.root)
        self.rFrame.grid(row=0, column=1, sticky="nswe")
        self.rFrame.grid_columnconfigure(0, weight=1)
        self.rFrame.grid_rowconfigure(0, weight=1)

    def show(self) -> None:
        """ Show window with user interface. """
        self.root.mainloop()
