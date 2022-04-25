from tkinter import (
    Tk,
    Frame,
    Canvas,
    Button,
    Label,
    Event,
    NW
)

from app.gui import (
    file_handling,
    image_view,
    control_panel,
    processing
)


class Window:
    """ Context class for user interface window. """
    # imported methods
    _selectFile = file_handling.selectFile
    _loadImage = file_handling.loadImage
    _saveImage = file_handling.saveImage

    _renderImage = image_view.renderImage
    _displayImageFromArray = image_view.displayImageFromArray
    _setDefaultImgZoom = image_view.setDefaultImgZoom
    _cropOutOfRender = image_view.cropOutOfRender
    _imageMouseWheel = image_view.imageMouseWheel

    _bindControlPanel = control_panel.bindControlPanel
    _bindPalettePicker = control_panel.bindPalettePicker
    _updatePalettePicker = control_panel.updatePalettePicker
    _bindDitheringPicker = control_panel.bindDitheringPicker
    _bindSubmit = control_panel.bindSubmit

    _pressSubmit = processing.pressSubmit
    _processImage = processing.processImage
    _processingDone = processing.processingDone

    def __init__(self, name: str = "Window") -> None:
        # instance variables
        self.displayedImg = None
        self.palettes = ["Median Cut", "Bit Stripping"]
        self.ditherings = ["Floyd-Steinberg", "Jarvis", "Stucki"]

        # initial settings
        self.root = Tk()
        self.root.title(name)
        self.root.geometry("1024x720")
        self.root.minsize(1024, 720)

        # bind components
        self._configureFrames()
        self._bindCanvas()
        self._bindFileSelector()
        self._bindControlPanel()

        # bind events
        self.root.bind("<Configure>", self._windowResize)
        self.canvas.bind("<MouseWheel>", self._imageMouseWheel)
        self.canvas.bind("<Button-4>", self._imageMouseWheel)
        self.canvas.bind("<Button-5>", self._imageMouseWheel)

    def _configureFrames(self) -> None:
        """ Create main grid layout with frames. """
        # configure grid (1x3)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # configure left frame (0, 0)
        self.lFrame = Frame(self.root)
        self.lFrame.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

        # configure right frame (0, 1:2)
        self.rFrame = Frame(self.root)
        self.rFrame.grid(row=0, column=1, columnspan=2, sticky="nswe")
        self.rFrame.grid_columnconfigure(0, weight=1)
        self.rFrame.grid_rowconfigure(0, weight=1)

    def _bindCanvas(self) -> None:
        """ Bind canvas element to main window. """
        self.canvas = Canvas(self.rFrame, bg="#1e1e1e")
        self.canvas.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

    def _bindFileSelector(self) -> None:
        """ Bind file selector to main window. """
        # button for file selection
        self.b_selectFile = Button(
            self.lFrame, text='Select image',  command=self._selectFile)
        self.b_selectFile.pack(side="top", anchor=NW, padx=10, pady=10)

        # label with selected file name
        self.l_selectedFile = Label(self.lFrame, text="File not selected",
                                    font=('TkDefaultFont', 8))
        self.l_selectedFile.pack(side="top", anchor=NW, padx=10, pady=10)

    def _windowResize(self, _: Event) -> None:
        """ Adjust displayed image to resized window. """
        if self.displayedImg is not None:
            self._renderImage()

    def show(self) -> None:
        """ Show window with user interface. """
        self.root.mainloop()
