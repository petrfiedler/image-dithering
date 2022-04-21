from tkinter import (Tk,
                     Frame,
                     Canvas,
                     Button,
                     Label,
                     NW)

from app.gui import file_handling


class Window:
    # imported methods
    selectFile = file_handling.selectFile
    loadImage = file_handling.loadImage

    def __init__(self):
        # initial settings
        self.root = Tk()
        self.root.title('Image Dithering')
        self.root.geometry("1024x720")
        self.root.minsize(1024, 720)

        # bind components
        self.configureFrames()
        self.bindCanvas()
        self.bindFileSelector()

    def configureFrames(self):
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

    def bindCanvas(self):
        self.canvas = Canvas(self.rFrame, bg="#1e1e1e")
        self.canvas.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

    def bindFileSelector(self):
        # button for file selection
        self.b_selectFile = Button(
            self.lFrame, text='Select image',  command=self.selectFile)
        self.b_selectFile.pack(side="top", anchor=NW, padx=10, pady=10)

        # label with selected file name
        self.l_selectedFile = Label(self.lFrame, text="File not selected",
                                    font=('TkDefaultFont', 8))
        self.l_selectedFile.pack(side="top", anchor=NW, padx=10, pady=10)

    def show(self):
        self.root.mainloop()
