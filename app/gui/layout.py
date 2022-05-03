from tkinter import Frame


def configureFrames(self) -> None:
    """ Create main grid layout with frames. """

    # configure grid (1x3)
    self.root.grid_columnconfigure(0)
    self.root.grid_columnconfigure(1, weight=1)
    self.root.grid_rowconfigure(0, weight=1)

    # configure left frame (0, 0)
    self.lFrame = Frame(self.root, width=384)

    self.lFrame.grid(
        row=0,
        column=0,
        sticky="nwe",
        padx=20,
        pady=20
    )

    # configure right frame (0, 1:2)
    self.rFrame = Frame(self.root)

    self.rFrame.grid(row=0, column=1, sticky="nswe")

    self.rFrame.grid_columnconfigure(0, weight=1)
    self.rFrame.grid_rowconfigure(0, weight=1)
