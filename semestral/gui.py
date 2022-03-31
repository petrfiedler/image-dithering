from tkinter import Tk, Button, Canvas, PhotoImage, NW, CENTER, Label, Frame
from tkinter import filedialog as fd
from PIL import Image,ImageTk
import re
import math

root = Tk()
root.geometry("1000x800")
root.grid_columnconfigure(0, weight = 1)
root.grid_columnconfigure(1, weight = 1)
root.grid_columnconfigure(2, weight = 1)
root.grid_rowconfigure(0, weight = 1)


leftFrame = Frame(root)
leftFrame.grid(row=0, column=0, sticky="nswe", padx = 20, pady = 20)

rightFrame = Frame(root)
rightFrame.grid(row=0, column=1, columnspan=2, sticky="nswe")
rightFrame.grid_columnconfigure(0, weight = 1)
rightFrame.grid_rowconfigure(0, weight = 1)

rootHeight = root.winfo_height()
rootWidth = root.winfo_width()
print(rootWidth, rootHeight)

canvas = Canvas(rightFrame, bg="#1e1e1e")
canvas.grid(row=0, column=0, sticky="nswe", padx = 20, pady = 20)

percentage = 1
# resize image to fit canvas
def setDefaultImageSize(img, cWidth, cHeight):
    # fit to width
    if cWidth / cHeight < img.size[0] / img.size[1]:
        percent = cWidth/float(img.size[0])
        if percent > 1:
            percent = math.floor(percent)
        else:
            percent = math.ceil(percent)
        newWidth = int((float(img.size[0])*float(percent)))
        newHeight = int((float(img.size[1])*float(percent)))
        img = img.resize((newWidth,newHeight), resample=Image.NEAREST)
    # fit to height
    else:
        percent = cHeight/float(img.size[1])
        if percent > 1:
            percent = math.floor(percent)
        else:
            percent = math.ceil(percent)
        newWidth = int((float(img.size[0])*float(percent)))
        newHeight = int((float(img.size[1])*float(percent)))
        img = img.resize((newWidth,newHeight), resample=Image.NEAREST)
    return img

rawImg = None

def selectFile():
    fileTypes = (
        ('png image', '*.png'),
        ('jpg image', '*.jpg'),
        ('all files', '*')
    )
    global rawImg
    fileName = fd.askopenfilename(title='Select image', filetypes=fileTypes)
    if fileName:
        global percentage
        print(fileName)
        shortFileName = re.findall(r'/[^/]+$',fileName)[0][1:]
        l_selectedFile.config(text=shortFileName)

        # display image
        rawImg = Image.open(fileName)
        rawImg = setDefaultImageSize(rawImg, canvas.winfo_width(), canvas.winfo_height())
        img = ImageTk.PhotoImage(rawImg)
        canvas.delete("all")
        imageid = canvas.create_image(canvas.winfo_width()/2,canvas.winfo_height()/2,anchor='center',image=img)
        canvas.lower(imageid)
        canvas.imagetk = img
        percentage = 1


def resize():
    img = rawImg
    global percentage
    if percentage > 1:
        cw = canvas.winfo_width()
        ch = canvas.winfo_height()
        iw = int((float(img.size[0])*float(percentage)))
        ih = int((float(img.size[1])*float(percentage)))
        print("cw:",cw,"ch:",ch,"ih:",ih,"iw:",iw)
        print("before crop",img.size)
        img = img.crop((
            math.floor(((iw - cw)/2)/percentage ) if cw < iw else 0,
            math.floor(((ih - ch)/2)/percentage) if ch < ih else 0,
            math.ceil(((iw - cw)/2 + cw)/percentage) if cw < iw else img.size[0],
            math.ceil(((ih - ch)/2 + ch)/percentage) if ch < ih else img.size[1],
        ))
        print("after crop",img.size)
        newWidth = int((float(img.size[0])*float(percentage)))
        newHeight = int((float(img.size[1])*float(percentage)))
    else:
        newWidth = int((float(img.size[0])*float(percentage)))
        newHeight = int((float(img.size[1])*float(percentage)))
    if percentage > 1:
        img = img.resize((newWidth,newHeight), resample=Image.NEAREST)
    else:
        img = img.resize((newWidth,newHeight), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    canvas.delete("all")
    imageid = canvas.create_image(canvas.winfo_width()/2,canvas.winfo_height()/2,anchor='center',image=img)
    canvas.lower(imageid)
    canvas.imagetk = img

def mouse_wheel(event):
    global percentage
    # respond to Linux or Windows wheel event
    if event.num == 5 or event.delta == -120:
        if min(rawImg.size)*percentage > 30:
            percentage /= 1.5
            if percentage > 1:
                percentage = math.floor(percentage)
            resize()
    if event.num == 4 or event.delta == 120:
        if max(rawImg.size)*percentage < 30000:
            percentage *= 1.5
            if percentage > 1:
                percentage = math.ceil(percentage)
            resize()
    print(percentage)

# with Windows OS
canvas.bind("<MouseWheel>", mouse_wheel)
# with Linux OS
canvas.bind("<Button-4>", mouse_wheel)
canvas.bind("<Button-5>", mouse_wheel)

# button for file selection
b_selectFile = Button(leftFrame, text='Select image',  command=selectFile)
b_selectFile.pack(side="top", anchor=NW, padx=10, pady=10)

# label with selected file name
l_selectedFile = Label(leftFrame, text="File not selected", font=('TkDefaultFont',8))
l_selectedFile.pack(side="top", anchor=NW, padx=10, pady=10)

root.mainloop()