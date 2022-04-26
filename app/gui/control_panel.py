from tkinter import (Label,
                     OptionMenu,
                     StringVar,
                     Frame,
                     Button,
                     Scale,
                     NW)
from tkinter.ttk import Separator


def bindControlPanel(self):
    """ Bind control panel to main window. """
    self._bindFileSelector()
    self._bindPalettePicker()
    self._bindDitheringPicker()
    self._bindButtons()
    self._bindReset()
    self._bindSubmit()


def bindFileSelector(self) -> None:
    """ Bind file selector to main window. """
    # button for file selection
    self.b_selectFile = Button(
        self.lFrame, text='Select image',  command=self._selectFile)
    self.b_selectFile.pack(side="top", anchor=NW, padx=10, pady=10)

    # label with selected file name
    self.l_selectedFile = Label(self.lFrame, text="File not selected")
    self.l_selectedFile.pack(side="top", anchor=NW, padx=10, pady=10)


def bindPalettePicker(self):
    """ Bind palette picker to main window. """
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
        self.s_palleteOptions.config(
            length=256,
            orient="horizontal",
            bg=self.BG, fg=self.FG, highlightthickness=0,
            sliderrelief="flat", activebackground=self.BG)
        self.s_palleteOptions.pack(side="top", anchor=NW, padx=10)


def bindDitheringPicker(self):
    """ Bind dithering picker to main window. """
    separator = Separator(self.lFrame, orient='horizontal')
    separator.pack(fill='x', pady=30)

    self.l_ditheringPicker = Label(self.lFrame, text="Dithering algorithm:")
    self.l_ditheringPicker.pack(side="top", anchor=NW, padx=10)

    # dropdown menu
    self.pickedDithering = StringVar()
    self.pickedDithering.set(self.ditherings[0])

    self.om_ditheringPicker = OptionMenu(
        self.lFrame, self.pickedDithering, *self.ditherings)
    self.om_ditheringPicker.pack(side="top", anchor=NW, padx=10, pady=10)


def bindButtons(self):
    separator = Separator(self.lFrame, orient='horizontal')
    separator.pack(fill='x', pady=30)
    self.f_buttons = Frame(self.lFrame)
    self.f_buttons.columnconfigure(0, weight=1)
    self.f_buttons.columnconfigure(1, weight=1)
    self.f_buttons.rowconfigure(0)
    self.f_buttons.rowconfigure(1)
    self.f_buttons.pack(side="top", anchor=NW, fill='x')


def bindSubmit(self):
    """ Bind submit button to main window. """
    self.b_submit = Button(self.f_buttons, text="Dither",
                           command=self._pressSubmit)
    self.b_submit["state"] = "disabled"
    self.b_submit.grid(row=0, column=1, sticky="e")
    self.l_submit = Label(self.f_buttons)
    self.l_submit.grid(row=1, column=1, columnspan=2, sticky="e", pady=10)


def bindReset(self) -> None:
    """ Bind reset button to main window. """
    self.b_reset = Button(
        self.f_buttons, text='Reset Image',  command=self._reset,
        state="disabled")
    self.b_reset.grid(row=0, column=0, sticky="w")
