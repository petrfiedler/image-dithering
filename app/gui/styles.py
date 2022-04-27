from tkinter import (RIGHT, PhotoImage)
from pathlib import Path


def loadStyleConstants(self):
    # colors
    self.BG = "#444444"
    self.BG_DARKER = "#222222"
    self.FG = "#ffffff"

    # menu indicator icons
    currentDir = Path(__file__).parent.resolve()
    self.imgDownArrow = PhotoImage(
        master=self.root, file=f"{currentDir}/img/dwn.png")
    self.imgUpArrow = PhotoImage(
        master=self.root, file=f"{currentDir}/img/up.png")


def applyStyles(self):

    # root
    self.root.config(
        bg=self.BG
    )

    # left frame
    self.lFrame.config(
        bg=self.BG
    )

    # right frame
    self.rFrame.config(
        bg=self.BG
    )

    # canvas
    self.canvas.config(
        bg=self.BG_DARKER,
        highlightthickness=0
    )

    # file selector button
    self.b_selectFile.config(
        bg=self.BG,
        fg=self.FG,
        activebackground=self.BG_DARKER,
        activeforeground=self.FG,
        borderwidth=0,
        highlightbackground=self.BG_DARKER
    )

    # file selector label
    self.l_selectedFile.config(
        font=('TkDefaultFont', 8),
        bg=self.BG,
        fg=self.FG
    )

    # palette picker label
    self.l_palettePicker.config(
        font=('TkDefaultFont', 12),
        bg=self.BG,
        fg=self.FG
    )

    # palette picker dropdown menu
    self.om_palettePicker.config(
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
    self.om_palettePicker["menu"].config(
        bg=self.BG,
        fg=self.FG,
        activebackground=self.BG_DARKER,
        activeforeground=self.FG,
        borderwidth=0,
        postcommand=lambda:
            self.om_palettePicker.configure(image=self.imgUpArrow)
    )
    self.om_palettePicker["menu"].bind(
        '<Unmap>',
        lambda _:
            self.om_palettePicker.configure(image=self.imgDownArrow)
    )

    # dithering picker label
    self.l_ditheringPicker.config(
        font=('TkDefaultFont', 12),
        bg=self.BG,
        fg=self.FG
    )

    # dithering picker dropdown menu
    self.om_ditheringPicker.config(
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
    self.om_ditheringPicker["menu"].config(
        bg=self.BG,
        fg=self.FG,
        activebackground=self.BG_DARKER,
        activeforeground=self.FG,
        borderwidth=0,
        postcommand=lambda:
            self.om_ditheringPicker.configure(image=self.imgUpArrow)
    )
    self.om_ditheringPicker["menu"].bind(
        '<Unmap>',
        lambda _:
        self.om_ditheringPicker.configure(image=self.imgDownArrow)
    )

    # buttons frame
    self.f_buttons.config(
        bg=self.BG
    )

    # reset button
    self.b_reset.config(
        bg=self.BG,
        fg=self.FG,
        activebackground=self.BG_DARKER,
        activeforeground=self.FG,
        borderwidth=0,
        highlightbackground=self.BG_DARKER
    )

    # submit button
    self.b_submit.config(
        bg=self.BG,
        fg=self.FG,
        activebackground=self.BG_DARKER,
        activeforeground=self.FG,
        borderwidth=0,
        highlightbackground=self.BG_DARKER
    )

    # submit label
    self.l_submit.config(
        bg=self.BG,
        fg=self.FG
    )

    # palette options frame
    self.paletteOptions.config(
        bg=self.BG
    )

    # dithering options frame
    self.ditheringOptions.config(
        bg=self.BG
    )
