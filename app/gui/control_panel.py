from tkinter import (
    Label,
    Frame,
    Button,
    NW
)
from tkinter.ttk import Separator


def bindControlPanel(self) -> None:
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
        self.lFrame,
        text='Select image',
        command=self._selectFile
    )

    self.b_selectFile.pack(side="top", anchor=NW, padx=10, pady=10)

    # label with selected file name
    self.l_selectedFile = Label(
        self.lFrame,
        text="File not selected"
    )

    self.l_selectedFile.pack(side="top", anchor=NW, padx=10, pady=10)


def bindButtons(self) -> None:
    """ Bind Reset / Submit buttons segment to main window. """

    # separator line
    separator = Separator(
        self.lFrame,
        orient='horizontal'
    )

    separator.pack(fill='x', pady=30)

    # buttons frame
    self.f_buttons = Frame(self.lFrame)

    self.f_buttons.columnconfigure(0, weight=1)
    self.f_buttons.columnconfigure(1, weight=1)
    self.f_buttons.rowconfigure(0)
    self.f_buttons.rowconfigure(1)

    self.f_buttons.pack(side="top", anchor=NW, fill='x')


def bindSubmit(self) -> None:
    """ Bind submit button to main window. """

    # submit button
    self.b_submit = Button(
        self.f_buttons,
        text="Dither",
        command=self._pressSubmit,
        width=10,
        state="disabled"
    )

    self.b_submit.grid(row=0, column=1, sticky="e", padx=(40, 0))

    # status text under submit button
    self.l_submit = Label(self.f_buttons)

    self.l_submit.grid(row=1, column=1, columnspan=2, sticky="e", pady=10)


def bindReset(self) -> None:
    """ Bind reset button to main window. """

    self.b_reset = Button(
        self.f_buttons,
        text='Reset Image',
        command=self._reset,
        state="disabled"
    )

    self.b_reset.grid(row=0, column=0, sticky="w")
