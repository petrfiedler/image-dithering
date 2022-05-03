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


def bindDitheringPicker(self) -> None:
    """ Bind dithering picker to main window. """

    # available dithering algorithms
    self.ditherings = (
        "Error Diffusion",
        "Bayer"
    )

    # separator line
    separator = Separator(
        self.lFrame,
        orient='horizontal'
    )

    separator.pack(fill='x', pady=30)

    # dithering picker label
    self.l_ditheringPicker = Label(
        self.lFrame,
        text="Dithering algorithm:"
    )

    self.l_ditheringPicker.pack(side="top", anchor=NW, padx=10)

    # dropdown menu with dithering algorithms
    self.pickedDithering = StringVar()
    self.pickedDithering.set(self.ditherings[0])

    self.om_ditheringPicker = OptionMenu(
        self.lFrame,
        self.pickedDithering,
        *self.ditherings,
        command=self._updateDitheringPicker
    )

    self.om_ditheringPicker.pack(side="top", anchor=NW, padx=10, pady=10)

    # dithering options frame
    self.ditheringOptions = Frame(self.lFrame)

    self.ditheringOptions.pack(side="top", anchor=NW)

    # display options of default dithering algorithm
    self._updateDitheringPicker(self.ditherings[0])


def updateDitheringPicker(self, option: str) -> None:
    """ Update dithering picker options based on picked algorithm. """

    # clear old frame content
    for element in self.ditheringOptions.winfo_children():
        element.destroy()

    # Bayer dithering options (treshold size)
    if option == "Bayer":

        # Bayer treshold size label
        self.l_ditheringOptions = Label(
            self.ditheringOptions,
            text="Treshold map size:"
        )

        self.l_ditheringOptions.config(
            font=('TkDefaultFont', 8),
            bg=self.BG,
            fg=self.FG
        )

        self.l_ditheringOptions.pack(
            side="top",
            anchor=NW,
            padx=10,
            pady=(10, 0)
        )

        # Bayer treshold size scale
        self.s_ditheringOptions = Scale(
            self.ditheringOptions,
            from_=1,
            to=10
        )

        self.s_ditheringOptions.set(3)  # default value

        self.s_ditheringOptions.config(
            length=256,
            orient="horizontal",
            bg=self.BG,
            fg=self.FG,
            highlightthickness=0,
            sliderrelief="flat",
            activebackground=self.BG
        )

        self.s_ditheringOptions.pack(side="top", anchor=NW, padx=10)

    # Error Diffusion dithering options (distribution map)
    if option == "Error Diffusion":

        # Error distribution map label
        self.l_ditheringOptions = Label(
            self.ditheringOptions,
            text="Error distribution map:"
        )

        self.l_ditheringOptions.config(
            font=('TkDefaultFont', 8),
            bg=self.BG,
            fg=self.FG
        )

        self.l_ditheringOptions.pack(
            side="top",
            anchor=NW,
            padx=10,
            pady=(10, 0)
        )

        # Error distribution map dropdown menu
        maps = ERROR_DIFFUSION_MAPS.keys()

        self.pickedDitheringOption = StringVar()
        self.pickedDitheringOption.set(list(maps)[0])

        self.om_ditheringOptions = OptionMenu(
            self.ditheringOptions,
            self.pickedDitheringOption,
            *maps
        )

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
