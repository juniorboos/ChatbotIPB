import tkinter
from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("Map")
Image.MAX_IMAGE_PIXELS = 1024000000
# root.geometry("960x720")
# root.resizable(width=FALSE, height= FALSE)

floor = Image.open("Blueprint/PISO -1.png")
# floorResized = ImageTk.PhotoImage(floor.resize((1000,1000)))
floorResized = floor.resize((1000,1000))

locationIcon = Image.open("Blueprint/location_icon.png")

# floorResized.paste(locationIcon, (500, 400), locationIcon)
floorResized.paste(locationIcon, (710, 360), locationIcon)

tkimage = ImageTk.PhotoImage(floorResized)

panel1 = Label(root, image=tkimage)
panel1.grid(row=0, column=2, sticky=E)
# my_label = Label(image=floorResized)
# my_label.pack()


root.mainloop()

