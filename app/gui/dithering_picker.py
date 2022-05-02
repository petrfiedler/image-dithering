from tkinter import (
    Label,
    Scale,
    OptionMenu,
    Frame,
    StringVar,
    NW,
    RIGHT
)

from tkinter.ttk import Separator

from app.src.dithering.error_diffusion_maps import ERROR_DIFFUSION_MAPS


def bindDitheringPicker(self):
    """ Bind dithering picker to main window. """

    self.ditherings = [
        "Error Diffusion",
        "Bayer"
    ]

    separator = Separator(self.lFrame, orient='horizontal')
    separator.pack(fill='x', pady=30)

    self.l_ditheringPicker = Label(self.lFrame, text="Dithering algorithm:")
    self.l_ditheringPicker.pack(side="top", anchor=NW, padx=10)

    # dropdown menu
    self.pickedDithering = StringVar()
    self.pickedDithering.set(self.ditherings[0])

    self.om_ditheringPicker = OptionMenu(
        self.lFrame, self.pickedDithering, *self.ditherings,
        command=self._updateDitheringPicker)
    self.om_ditheringPicker.pack(side="top", anchor=NW, padx=10, pady=10)

    # options
    self.ditheringOptions = Frame(self.lFrame)
    self.ditheringOptions.pack(side="top", anchor=NW)

    self._updateDitheringPicker(self.ditherings[0])


def updateDitheringPicker(self, option):
    """ Update dithering picker options based on picked algorithm. """
    for element in self.ditheringOptions.winfo_children():
        element.destroy()

    if option == "Bayer":
        # bayer label
        self.l_ditheringOptions = Label(self.ditheringOptions,
                                        text="Treshold map size:")
        self.l_ditheringOptions.config(
            font=('TkDefaultFont', 8),
            bg=self.BG,
            fg=self.FG
        )
        self.l_ditheringOptions.pack(
            side="top", anchor=NW, padx=10, pady=(10, 0))

        # bayer scale
        self.s_ditheringOptions = Scale(self.ditheringOptions, from_=1, to=10)
        self.s_ditheringOptions.set(3)
        self.s_ditheringOptions.config(
            length=256,
            orient="horizontal",
            bg=self.BG, fg=self.FG, highlightthickness=0,
            sliderrelief="flat", activebackground=self.BG)
        self.s_ditheringOptions.pack(side="top", anchor=NW, padx=10)

    if option == "Error Diffusion":
        # error diffusion label
        self.l_ditheringOptions = Label(self.ditheringOptions,
                                        text="Error distribution map:")
        self.l_ditheringOptions.config(
            font=('TkDefaultFont', 8),
            bg=self.BG,
            fg=self.FG
        )
        self.l_ditheringOptions.pack(
            side="top", anchor=NW, padx=10, pady=(10, 0))

        # error diffusion picker
        maps = ERROR_DIFFUSION_MAPS.keys()
        self.pickedDitheringOption = StringVar()
        self.pickedDitheringOption.set(list(maps)[0])
        self.om_ditheringOptions = OptionMenu(
            self.ditheringOptions, self.pickedDitheringOption, *maps)
        self.om_ditheringOptions.config(
            bg=self.BG,
            fg=self.FG,
            activebackground=self.BG_DARKER,
            activeforeground=self.FG,
            borderwidth=0,
            highlightthickness=1,
            indicatoron=0,
            compound=RIGHT,
            image=self.imgDownArrow,
            highlightbackground=self.BG_DARKER
        )
        self.om_ditheringOptions["menu"].config(
            bg=self.BG,
            fg=self.FG,
            activebackground=self.BG_DARKER,
            activeforeground=self.FG,
            borderwidth=0,
            postcommand=lambda:
                self.om_ditheringOptions.configure(image=self.imgUpArrow)
        )
        self.om_ditheringOptions["menu"].bind(
            '<Unmap>',
            lambda _:
            self.om_ditheringOptions.configure(image=self.imgDownArrow)
        )
        self.om_ditheringOptions.pack(side="top", anchor=NW, padx=10, pady=10)
