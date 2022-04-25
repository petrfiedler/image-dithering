from tkinter import (Label,
                     OptionMenu,
                     StringVar,
                     Frame,
                     Button,
                     Scale,
                     NW, NE)
from tkinter.ttk import Separator


def bindControlPanel(self):
    """ Bind control panel to main window. """
    self._bindFileSelector()
    self._bindPalettePicker()
    self._bindDitheringPicker()
    self._bindSubmit()


def bindFileSelector(self) -> None:
    """ Bind file selector to main window. """
    # button for file selection
    self.b_selectFile = Button(
        self.lFrame, text='Select image',  command=self._selectFile)
    self.b_selectFile.pack(side="top", anchor=NW, padx=10, pady=10)

    # label with selected file name
    self.l_selectedFile = Label(self.lFrame, text="File not selected",
                                font=('TkDefaultFont', 8))
    self.l_selectedFile.pack(side="top", anchor=NW, padx=10, pady=10)


def bindPalettePicker(self):
    """ Bind palette picker to main window. """
    separator = Separator(self.lFrame, orient='horizontal')
    separator.pack(fill='x', pady=30)

    self.l_palettePicker = Label(self.lFrame, text="Color palette:",
                                 font=('TkDefaultFont', 12))
    self.l_palettePicker.pack(side="top", anchor=NW, padx=10)

    # dropdown menu
    self.pickedPalette = StringVar()
    self.pickedPalette.set(self.palettes[0])

    self.om_palettePicker = OptionMenu(
        self.lFrame, self.pickedPalette, *self.palettes,
        command=self._updatePalettePicker)
    self.om_palettePicker.pack(side="top", anchor=NW, padx=10, pady=10)

    # palette options
    self.paletteOptions = Frame(self.lFrame)
    self.paletteOptions.pack(side="top", anchor=NW)

    self._updatePalettePicker(self.pickedPalette.get())


def updatePalettePicker(self, option):
    """ Update palette picker options based on picked palette. """
    for element in self.paletteOptions.winfo_children():
        element.destroy()

    if option == "Median Cut":
        self.l_paletteOptions = Label(self.paletteOptions,
                                      text="Number of bits:",
                                      font=('TkDefaultFont', 8))
        self.l_paletteOptions.pack(
            side="top", anchor=NW, padx=10, pady=(10, 0))

        self.s_palleteOptions = Scale(
            self.paletteOptions, from_=1, to=16, length=256,
            orient="horizontal")
        self.s_palleteOptions.pack(side="top", anchor=NW, padx=10)


def bindDitheringPicker(self):
    """ Bind dithering picker to main window. """
    separator = Separator(self.lFrame, orient='horizontal')
    separator.pack(fill='x', pady=30)

    self.l_ditheringPicker = Label(self.lFrame, text="Dithering algorithm:",
                                   font=('TkDefaultFont', 12))
    self.l_ditheringPicker.pack(side="top", anchor=NW, padx=10)

    # dropdown menu
    self.pickedDithering = StringVar()
    self.pickedDithering.set(self.ditherings[0])

    self.om_ditheringPicker = OptionMenu(
        self.lFrame, self.pickedDithering, *self.ditherings)
    self.om_ditheringPicker.pack(side="top", anchor=NW, padx=10, pady=10)


def bindSubmit(self):
    """ Bind submit button to main window. """
    self.b_submit = Button(self.lFrame, text="Dither",
                           command=self._pressSubmit)
    self.b_submit["state"] = "disabled"
    self.l_submit = Label(self.lFrame)
    self.l_submit.pack(side="bottom", anchor=NE, padx=10, pady=(10, 10))
    self.b_submit.pack(side="bottom", anchor=NE, padx=10, pady=(128, 0))
