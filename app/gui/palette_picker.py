from tkinter import (
    Label,
    Scale,
    OptionMenu,
    Frame,
    StringVar,
    NW
)

from tkinter.ttk import Separator


def bindPalettePicker(self):
    """ Bind palette picker to main window. """

    self.palettes = [
        "Bit Stripping",
        "Websafe",
        "Median Cut"
    ]

    separator = Separator(self.lFrame, orient='horizontal')
    separator.pack(fill='x', pady=30)

    self.l_palettePicker = Label(self.lFrame, text="Color palette:")
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

    if option == "Bit Stripping":
        # bit stripping label
        self.l_paletteOptions = Label(self.paletteOptions,
                                      text="Stripping level:")
        self.l_paletteOptions.config(
            font=('TkDefaultFont', 8),
            bg=self.BG,
            fg=self.FG
        )
        self.l_paletteOptions.pack(
            side="top", anchor=NW, padx=10, pady=(10, 0))

        # bit stripping scale
        self.s_palleteOptions = Scale(self.paletteOptions, from_=1, to=7)
        self.s_palleteOptions.set(5)
        self.s_palleteOptions.config(
            length=256,
            orient="horizontal",
            bg=self.BG, fg=self.FG, highlightthickness=0,
            sliderrelief="flat", activebackground=self.BG)
        self.s_palleteOptions.pack(side="top", anchor=NW, padx=10)

    if option == "Median Cut":
        # median cut label
        self.l_paletteOptions = Label(self.paletteOptions,
                                      text="Number of bits:")
        self.l_paletteOptions.config(
            font=('TkDefaultFont', 8),
            bg=self.BG,
            fg=self.FG
        )
        self.l_paletteOptions.pack(
            side="top", anchor=NW, padx=10, pady=(10, 0))

        # median cut scale
        self.s_palleteOptions = Scale(self.paletteOptions, from_=1, to=10)
        self.s_palleteOptions.set(5)
        self.s_palleteOptions.config(
            length=256,
            orient="horizontal",
            bg=self.BG, fg=self.FG, highlightthickness=0,
            sliderrelief="flat", activebackground=self.BG)
        self.s_palleteOptions.pack(side="top", anchor=NW, padx=10)
